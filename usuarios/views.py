from django.shortcuts import render, redirect
from .forms import cadastroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def cadastroUser(request):
    form = cadastroForm()
    if request.method == 'POST':
        form = cadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'usuarios/cadastro.html', {'form': form})

def loginUser(request):
    form = AuthenticationForm(request, data=request.POST)

    if form.is_valid():
        user = form.get_user()
        auth.login(request, user)
        return redirect('home')
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def logoutUser(request):
    auth.logout(request)
    return redirect('login')