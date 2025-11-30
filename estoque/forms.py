from django import forms
from .models import Estoque, Maquina

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = '__all__'
        widgets = {
            "codigo": forms.TextInput(attrs={
                "class": "input-field",
                "placeholder": "Digite o código",
                "maxlength": "25",
            }),
            "nome": forms.TextInput(attrs={
                "class": "input-field",
                "placeholder": "Digite o nome",
                "maxlength": "25",
            }),
            "marca": forms.TextInput(attrs={
                "class": "input-field",
                "placeholder": "Digite a marca",
                "maxlength": "15",
            }),
            "fornecedor": forms.TextInput(attrs={
                "class": "input-field",
                "placeholder": "Digite o fornecedor",
                "maxlength": "15",
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "input-field",
                "placeholder": "Digite a quantidade",
            }),
            "preco": forms.NumberInput(attrs={
                "class": "input-field",
                "placeholder": "Digite o preço",
                "step": "0.01",
            }),
            "qtd_min": forms.NumberInput(attrs={
                "class": "input-field",
                "placeholder": "Mínimo",
            }),
            "qtd_max": forms.NumberInput(attrs={
                "class": "input-field",
                "placeholder": "Máximo",
            }),
            "descricao": forms.Textarea(attrs={
                "class": "input-field textarea-field",
                "placeholder": "Digite uma descrição",
            }),
        }



class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        exclude = ['pecas'] 
        fields = '__all__'   

