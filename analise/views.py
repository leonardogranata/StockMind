# Em analise/views.py

import json
import pandas as pd # Certifique-se de que o pandas está importado
from django.shortcuts import render
from estoque.models import Estoque
from analise.ia import prever_consumo # Importe sua função de previsão

def previsao(request):
    # Pega o nome de todos os itens do banco de dados para popular o <select>
    itens = Estoque.objects.all()
    nomes_itens = [item.nome for item in itens]
    
    # Dicionário para armazenar as previsões de todos os itens
    previsoes_todos_itens = {}

    for item_nome in nomes_itens:
        # Chama sua função de previsão para cada item
        previsao_df = prever_consumo(item_nome, dias=15)

        # Pula para o próximo item se a previsão estiver vazia
        if previsao_df is None or previsao_df.empty:
            continue

        # Garante que a coluna de data ('ds') esteja como string no formato YYYY-MM-DD
        previsao_df['ds'] = pd.to_datetime(previsao_df['ds']).dt.strftime('%Y-%m-%d')
        
        # Seleciona apenas as colunas 'ds' (data) e 'yhat' (previsão)
        previsao_filtrada = previsao_df[['ds', 'yhat']]
        
        # Converte o DataFrame para uma lista de listas (ex: [['2025-10-15', 12.5], ...])
        dados_grafico = previsao_filtrada.values.tolist()
        
        # Adiciona os dados ao nosso dicionário principal
        previsoes_todos_itens[item_nome] = dados_grafico

    # Converte o dicionário inteiro para uma string JSON
    previsoes_json = json.dumps(previsoes_todos_itens)

    context = {
        'nomes_itens': nomes_itens,
        'previsoes_json': previsoes_json,
    }

    return render(request, 'analise/previsao.html', context)