from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from analise.models import Consumo
from .models import Estoque, Auditoria
from .forms import EstoqueForm
from django.utils import timezone
import json
from django.http import JsonResponse, HttpResponse
from decimal import Decimal
from django.contrib.auth.decorators import login_required


# CRUD

@login_required
def home(request):
    busca = request.GET.get('q')  # pega o texto digitado na busca
    if busca:
        itens = Estoque.objects.filter(nome__icontains=busca)
    else:
        itens = Estoque.objects.all()
    return render(request, 'estoque/home.html', {'itens': itens})


@login_required
def cadastroItem(request):
    if request.method == 'POST':
        form = EstoqueForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario_logado = request.user  # para auditoria
            item.save()
            return redirect('home')
    else:
        form = EstoqueForm()
    return render(request, 'estoque/cadastro.html', {'form': form})

@login_required
def editarItem(request, pk):
    estoque = get_object_or_404(Estoque, pk=pk)
    quantidade_anterior = estoque.quantidade
    item = get_object_or_404(Estoque, pk=pk)

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            novo_item = form.save(commit=False)
            diferenca = quantidade_anterior - novo_item.quantidade

            # se retirou item
            if diferenca > 0:
                hoje = timezone.now().date()
                consumo_existente = Consumo.objects.filter(item=estoque, data=hoje).first()

                if consumo_existente:
                    consumo_existente.quantidade += diferenca
                    consumo_existente.save()
                else:
                    Consumo.objects.create(
                        item=estoque,
                        quantidade=diferenca,
                        data=hoje,
                        usuario=request.user
                    )
            novo_item.save()
            return redirect('home')

    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'estoque/editar.html', {'form': form, 'estoque': estoque, 'item': item})

@login_required
def excluirItem(request, pk):
    estoque = get_object_or_404(Estoque, pk=pk)
    if request.method == 'POST':
        estoque.usuario_logado = request.user  # para auditoria
        estoque.delete()
        return redirect('home')
    return render(request, 'estoque/excluir.html', {'estoque': estoque})

# auditoria:
def auditoria_list(request):
    logs = Auditoria.objects.all().order_by('-data_hora')
    return render(request, 'estoque/auditoria_list.html', {'logs': logs})

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # ou str(obj) se quiser manter formato exato
        return super().default(obj)

@login_required
def exportar_json(request):
    dados = list(Estoque.objects.values())
    response = HttpResponse(
        json.dumps(dados, indent=4, ensure_ascii=False, cls=DecimalEncoder),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="estoque.json"'
    return response


# --- Importar ---
@login_required
def importar_json(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        dados = json.load(arquivo)

        for item in dados:
            item_id = item.pop('id', None)  # pega o ID e remove do dict

            # converte float/str para Decimal nos campos numéricos
            for campo in ['preco', 'qtd_min', 'qtd_max', 'quantidade']:
                if campo in item:
                    try:
                        item[campo] = Decimal(str(item[campo]))
                    except:
                        pass

            # se já existir, atualiza; senão, cria
            if item_id and Estoque.objects.filter(id=item_id).exists():
                Estoque.objects.filter(id=item_id).update(**item)
            else:
                Estoque.objects.create(**item)

    return redirect('home')