from django.shortcuts import render
from .ia import prever_consumo
from estoque.models import Estoque

def previsao(request):
    previsoes_itens = []

    itens = Estoque.objects.all()
    for item in itens:
        # gera a previsão (últimos 15 dias)
        previsao = prever_consumo(item.nome, 15)
        previsoes_itens.append({
            'item': item.nome,
            'previsao': previsao
        })

    return render(request, 'analise/previsao.html', {'previsoes_itens': previsoes_itens})
