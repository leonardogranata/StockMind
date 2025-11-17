from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from analise.models import Consumo
from .models import Estoque, Auditoria, Maquina
from .forms import EstoqueForm, MaquinaForm
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

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            novo_item = form.save(commit=False)

            # salva primeiro para garantir que o obj está persistido e tem pk definitivo
            novo_item.save()

            # calculo de diferença (consumo): se diminuiu, registra consumo
            diferenca = quantidade_anterior - novo_item.quantidade
            if diferenca > 0:
                hoje = timezone.now().date()
                consumo_existente = Consumo.objects.filter(item=novo_item, data=hoje).first()
                if consumo_existente:
                    consumo_existente.quantidade += diferenca
                    consumo_existente.save()
                else:
                    Consumo.objects.create(
                        item=novo_item,
                        quantidade=diferenca,
                        data=hoje,
                        usuario=request.user
                    )

            return redirect('home')
        else:
            # debug: imprime erros no console do servidor para tu ver
            print("FORM ERRORS:", form.errors)
    else:
        form = EstoqueForm(instance=estoque)

    return render(request, 'estoque/editar.html', {
        'form': form,
        'estoque': estoque,
        'item': estoque
    })


@login_required
def excluirItem(request, pk):
    estoque = get_object_or_404(Estoque, pk=pk)
    item = get_object_or_404(Estoque, pk=pk)
    if request.method == 'POST':
        estoque.usuario_logado = request.user
       
        estoque.delete()
        return redirect('home')
    return render(request, 'estoque/excluir.html', {'estoque': estoque, 'item': item})

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



# --- MÁQUINAS ---
@login_required
def maquinas(request):
    maquinas = Maquina.objects.all()
    return render(request, 'estoque/maquinas.html', {'maquinas': maquinas})

def cadastrarMaquina(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        localizacao = request.POST.get('localizacao')
        data_aquisicao = request.POST.get('data_aquisicao')
        status = request.POST.get('status')
        pecas_ids = request.POST.getlist('pecas')  # várias peças

        maquina = Maquina.objects.create(
            codigo=codigo,
            nome=nome,
            descricao=descricao,
            localizacao=localizacao,
            data_aquisicao=data_aquisicao if data_aquisicao else None,
            status=status
        )

        Auditoria.objects.create(
            usuario=request.user,
            tabela='Maquina',
            acao='INSERT',
            registro_id=maquina.id,
            descricao=(
                f"Máquina criada com sucesso.\n"
                f"Nome: {maquina.nome}\n"
                f"Código: {maquina.codigo}\n"
                f"Localização: {maquina.localizacao or 'Não informado'}\n"
                f"Status: {maquina.status}"
            )
        )

        if pecas_ids:
            maquina.pecas.set(pecas_ids)
        return redirect('maquinas')

    pecas = Estoque.objects.all()
    return render(request, 'estoque/cadastro_maquinas.html', {'pecas': pecas})

@login_required
def editar_maquina(request, id):
    maquina = get_object_or_404(Maquina, id=id)

    if request.method == 'POST':
        form = MaquinaForm(request.POST, instance=maquina)
        if form.is_valid():
            nova_maquina = form.save(commit=False)
            nova_maquina.save()
            
            # Atualiza o relacionamento com as peças, se enviado
            pecas_ids = request.POST.getlist('pecas')
            if pecas_ids:
                nova_maquina.pecas.set(pecas_ids)
            else:
                nova_maquina.pecas.clear()
            Auditoria.objects.create(
                usuario=request.user,
                tabela='Maquina',
                acao='UPDATE',
                registro_id=maquina.id,
                descricao=(
                    f"Máquina atualizada com novos dados.\n"
                    f"Nome: {maquina.nome}\n"
                    f"Código: {maquina.codigo}\n"
                    f"Localização: {maquina.localizacao or 'Não informado'}\n"
                    f"Status: {maquina.status}"
                )
            )
                    
            return redirect('maquinas')
    else:
        form = MaquinaForm(instance=maquina)

    pecas = Estoque.objects.all()
    return render(request, 'estoque/editar_maquina.html', {
        'form': form,
        'maquina': maquina,
        'pecas': pecas
    })

@login_required
def excluir_maquina(request, id):
    maquina = get_object_or_404(Maquina, id=id)

    if request.method == 'POST':
        
        Auditoria.objects.create(
            usuario=request.user,
            tabela='Maquina',
            acao='DELETE',
            registro_id=maquina.id,
            descricao=(
                f"Máquina removida.\n"
                f"Nome: {maquina.nome}\n"
                f"Código: {maquina.codigo}\n"
                f"Status anterior: {maquina.status}"
            )
        )
        maquina.delete()
        return redirect('maquinas')

    # Caso seja GET, mostra página de confirmação
    return render(request, 'estoque/excluir_maquina.html', {'maquina': maquina})

@login_required
def excluir_estoque(request, pk):
    item = get_object_or_404(Estoque, pk=pk)

    if request.method == 'POST':
        # Remove peça das máquinas associadas
        maquinas = Maquina.objects.filter(pecas=item)
        for m in maquinas:
            m.pecas.remove(item)

        Auditoria.objects.create(
            usuario=request.user,
            tabela='Estoque',
            acao='DELETE',
            registro_id=item.id,
            descricao=f"Peça deletada: {item.nome}"
        )
        item.delete()
        return redirect('home')

    return render(request, 'estoque/excluir.html', {'estoque': item})


def detalhes_maquina(request, id):
    maquina = get_object_or_404(Maquina, id=id)
    return render(request, 'estoque/detalhes_maquina.html', {'maquina': maquina})