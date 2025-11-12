from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class cadastroForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nome completo",
        help_text="Digite o nome e sobrenome do usuário."
    )

    is_superuser = forms.BooleanField(
        required=False,
        label="Usuário administrador?",
        help_text="Marque se este usuário deve ter permissões de administrador."
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'password1', 'password2', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '')
        if ' ' in full_name:
            parts = full_name.strip().split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
        if commit:
            user.save()
        return user


class editarUserForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nome completo"
    )

    class Meta:
        model = User
        fields = ['username', 'full_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '')
        if ' ' in full_name:
            parts = full_name.strip().split(' ', 1)
            user.first_name = parts[0]
            user.last_name = parts[1] if len(parts) > 1 else ''
        if commit:
            user.save()
        return user
        
