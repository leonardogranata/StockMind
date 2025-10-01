from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Estoque


@login_required
def home(request):
    return render(request, 'estoque/home.html')

@login_required
def cadastroItem(request):
    if request.method == 'POST':
        form = EstoqueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Item cadastrado com sucesso")
            return redirect('home')
    else:
        form = EstoqueForm()
    return render(request, './estoque/cadastro.html', {'form': form})

