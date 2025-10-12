from django.shortcuts import render
from .ia import prever_consumo

def previsao_view(request, item_nome):
    previsoes = prever_consumo(item_nome, 15)
    return render(request, 'analise/previsao.html', {'previsoes': previsoes, 'item_nome': item_nome})
