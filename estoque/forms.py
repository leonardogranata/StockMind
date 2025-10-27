from django import forms
from .models import Estoque, Maquina


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = '__all__'

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = '__all__'
