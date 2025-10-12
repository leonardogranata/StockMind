# Em analise/views.py

import json
from django.shortcuts import render
from estoque.models import Estoque

# AQUI ESTÁ A CORREÇÃO: Importe a sua função!
# Supondo que a função está em 'servicos_analise.py' no mesmo diretório
from analise.ia import prever_consumo

# Se o arquivo se chamasse utils.py, seria:
# from .utils import prever_consumo


def previsao(request):
    previsoes_itens = []

    itens = Estoque.objects.all()
    for item in itens:
        # Agora o Python sabe o que é 'prever_consumo'
        previsao_df = prever_consumo(item.nome, 15)

        # ... (o resto do seu código continua igual)
        if previsao_df is None or previsao_df.empty:
            continue

        previsao_df['ds'] = previsao_df['ds'].dt.strftime('%Y-%m-%d')
        previsao_filtrada = previsao_df[['ds', 'yhat']].copy()
        previsao_lista_para_json = previsao_filtrada.to_records(index=False).tolist()
        previsao_em_json = json.dumps(previsao_lista_para_json)
        previsao_para_tabela = previsao_filtrada.to_dict('records')

        previsoes_itens.append({
            'item': item.nome,
            'previsao_tabela': previsao_para_tabela,
            'previsao_json': previsao_em_json
        })

    context = {
        'previsoes_itens': previsoes_itens
    }

    return render(request, 'analise/previsao.html', context)