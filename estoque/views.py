from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Estoque, Auditoria
from .forms import EstoqueForm


# CRUD

@login_required
def home(request):
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
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            item = form.save(commit=False)
            item.usuario_logado = request.user  # para auditoria
            item.save()
            return redirect('home')  
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'estoque/editar.html', {'form': form, 'estoque': estoque})

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