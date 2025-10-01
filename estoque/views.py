from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Estoque
from .forms import EstoqueForm
from django.shortcuts import get_object_or_404, redirect

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
            form.save()
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
            form.save()
            return redirect('home')  
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'estoque/editar.html', {'form': form, 'estoque': estoque})

@login_required
def excluirItem(request, pk):
    estoque = get_object_or_404(Estoque, pk=pk)
    if request.method == 'POST':
        estoque.delete()
        return redirect('home')
    return render(request, 'estoque/excluir.html', {'estoque': estoque}) 


# -----------------
