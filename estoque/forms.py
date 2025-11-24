from django import forms
from .models import Estoque, Maquina

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = '__all__'
        widgets = {
            "codigo": forms.TextInput(attrs={"placeholder": "Digite o código", "maxlength": "25"}),
            "nome": forms.TextInput(attrs={"placeholder": "Digite o nome", "maxlength": "25"}),
            "descricao": forms.TextInput(attrs={"placeholder": "Descrição"}),
            "marca": forms.TextInput(attrs={"placeholder": "Digite a marca", "maxlength": "15"}),
            "fornecedor": forms.TextInput(attrs={"placeholder": "Digite o fornecedor", "maxlength": "15"}),
            "quantidade": forms.NumberInput(attrs={"placeholder": "Digite a quantidade"}),
            "preco": forms.NumberInput(attrs={"placeholder": "Digite o preço"}),
            "qtd_min": forms.NumberInput(attrs={"placeholder": "Mínimo"}),
            "qtd_max": forms.NumberInput(attrs={"placeholder": "Máximo"}),
        }

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        exclude = ['pecas'] 
        fields = '__all__'   

