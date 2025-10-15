from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class cadastroForm(UserCreationForm):
    is_superuser = forms.BooleanField(
        required=False,
        label="Usuário administrador?",
        help_text="Marque se este usuário deve ter permissões de administrador."
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_superuser')
