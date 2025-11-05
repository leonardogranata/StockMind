from .forms import cadastroForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from estoque.models import Auditoria
from django.contrib import messages


def loginUser(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "usuarios/login.html", {"form": form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastroUser(request):
    if request.method == "POST":
        form = cadastroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.is_staff = user.is_superuser 
            user.save()

            Auditoria.objects.create(
                usuario=request.user,
                tabela='User',
                acao='INSERT',
                registro_id=user.id,
                descricao=f"Usuário cadastrado: {user.username}, Superuser: {user.is_superuser}"
            )

            messages.success(request, f"Usuário '{user.username}' cadastrado com sucesso!")
            return redirect('listar')

        else:
            if 'password2' in form.errors:
                messages.error(request, "As senhas não coincidem!")
            else:
                messages.error(request, "Erro ao cadastrar usuário. Verifique os campos.")
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
@user_passes_test(lambda u: u.is_superuser)
def editarUser(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.usuario_logado = request.user  # para auditoria
            user.save()

            # Criar auditoria manual para user
            Auditoria.objects.create(
                usuario=request.user,
                tabela='User',
                acao='UPDATE',
                registro_id=user.id,
                descricao=f"Usuário atualizado: {user.username}, Email: {user.email}"
            )

            return redirect('listar')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'usuarios/editar.html', {'form': form, 'user': user})


@login_required
@user_passes_test(lambda u: u.is_superuser)  # só o superuser acessa
def excluirUser(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        # Criar auditoria manualmente antes de deletar
        Auditoria.objects.create(
            usuario=request.user,  # superuser que está deletando
            tabela='User',
            acao='DELETE',
            registro_id=user.id,
            descricao=f"Usuário deletado: {user.username}, Email: {user.email}"
        )
        user.delete()
        return redirect('listar')
    return render(request, 'usuarios/excluir.html', {'user': user})