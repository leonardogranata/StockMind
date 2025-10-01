from django.shortcuts import render, redirect
from .forms import cadastroForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.is_superuser)  # só o superuser acessa
def cadastroUser(request):
    if request.method == "POST":
        form = cadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = cadastroForm()
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

@login_required
@user_passes_test(lambda u: u.is_superuser)  # só o superuser acessa
def listarUsers(request):
    users = User.objects.all()
    return render(request, 'usuarios/listar.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)  # só o superuser acessa
def editarUser(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('listar')  # redireciona para a lista de usuários
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'usuarios/editar.html', {'form': form, 'user': user})


@login_required
@user_passes_test(lambda u: u.is_superuser)  # só o superuser acessa
def excluirUser(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('listar')
    return render(request, 'usuarios/excluir.html', {'user': user})
