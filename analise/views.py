import json
import pandas as pd 
from django.shortcuts import render
from estoque.models import Estoque
from analise.ia import prever_consumo 

def previsao(request):
    itens = Estoque.objects.all()
    nomes_itens = [item.nome for item in itens]
    previsoes_todos_itens = {}
    sugestoes = {}

    for item_nome in nomes_itens:
        previsao_df = prever_consumo(item_nome, dias=15)
        if previsao_df is None or previsao_df.empty:
            continue

        previsao_df['ds'] = pd.to_datetime(previsao_df['ds']).dt.strftime('%Y-%m-%d')
        previsao_filtrada = previsao_df[['ds', 'yhat']]
        dados_grafico = previsao_filtrada.values.tolist()
        previsoes_todos_itens[item_nome] = dados_grafico

        # --- Cálculo da sugestão ---
        try:
            item = Estoque.objects.get(nome=item_nome)
            estoque_atual = item.quantidade
            qtd_min = item.qtd_min
            consumo_diario = previsao_df['yhat'].mean()

            if consumo_diario > 0:
                dias_restantes = (estoque_atual - qtd_min) / consumo_diario
            else:
                dias_restantes = float('inf')

            if estoque_atual < qtd_min:
                sugestao = f"O estoque de {item_nome} está abaixo do nível mínimo! Compre imediatamente."
            elif estoque_atual == qtd_min:
                sugestao = f"O estoque de {item_nome} está no nível mínimo. Considere fazer uma nova compra logo."
            elif dias_restantes <= 5:
                sugestao = f"O estoque de {item_nome} deve atingir o nível mínimo em cerca de {dias_restantes:.1f} dias. Considere fazer uma nova compra."
            elif dias_restantes > 30:
                sugestao = f"{item_nome} está com baixo consumo e grande estoque. Evite novas compras por enquanto."
            else:
                sugestao = f"O estoque de {item_nome} está equilibrado conforme o consumo previsto."

            sugestoes[item_nome] = sugestao
        except Exception as e:
            sugestoes[item_nome] = f"Não foi possível gerar sugestão para {item_nome}."

    previsoes_json = json.dumps(previsoes_todos_itens)
    sugestoes_json = json.dumps(sugestoes)

    context = {
        'nomes_itens': nomes_itens,
        'previsoes_json': previsoes_json,
        'sugestoes_json': sugestoes_json,
    }

    return render(request, 'analise/previsao.html', context)
