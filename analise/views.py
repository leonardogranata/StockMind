import json
import pandas as pd 
from django.shortcuts import render
from estoque.models import Estoque
from analise.ia import prever_consumo 
from django.db.models import Sum
from .models import Consumo  

def dashboard(request):
    return render(request, 'analise/dashboard.html')

def itens_mais_usados(request):
    """
    Calcula o total consumido de cada item e prepara os dados para o gráfico.
    """
    # 1. Agrega os dados: Agrupa por nome do item e soma as quantidades consumidas.
    #    Ordena do mais consumido para o menos consumido e pega os TOP 10.
    dados_consumo = Consumo.objects.values('item__nome').annotate(
        total_consumido=Sum('quantidade')
    ).order_by('-total_consumido')[:10]  # Limita aos 10 itens mais usados

    # 2. Prepara as listas para o Chart.js
    labels = [item['item__nome'] for item in dados_consumo]
    data = [item['total_consumido'] for item in dados_consumo]
    
    # 3. Envia os dados para o template
    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'analise/maisUsados.html', context)

def previsao(request):
    itens = Estoque.objects.all()
    nomes_itens = [item.nome for item in itens]
    previsoes_todos_itens = {}
    sugestoes = {}

    for item_nome in nomes_itens:
        previsao_df = prever_consumo(item_nome, dias=15)
        if previsao_df is None:
            previsoes_todos_itens[item_nome] = []
            sugestoes[item_nome] = "Este item não possui dados suficientes (mínimo 2 dias de consumo)."
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

            # Se não há previsão válida
            if previsao_df is None or previsao_df.empty:
                sugestoes[item_nome] = (
                    f"O item {item_nome} não possui dados suficientes (mínimo 2 dias de consumo)."
                )
                continue

            previsoes_futuras = previsao_df['yhat'].tolist()

            dias = 0
            estoque_simulado = estoque_atual
            atingiu_minimo = False

            for consumo_dia in previsoes_futuras:
                if consumo_dia < 0:
                    consumo_dia = 0

                estoque_simulado -= consumo_dia
                dias += 1

                if estoque_simulado <= qtd_min:
                    atingiu_minimo = True
                    break

            # ---- Geração da sugestão ----

            if estoque_atual < qtd_min:
                sugestao = f"O estoque de {item_nome} está abaixo do mínimo! Compre imediatamente."

            elif estoque_atual == qtd_min:
                sugestao = f"O estoque de {item_nome} está exatamente no mínimo! Avalie comprar logo."

            elif atingiu_minimo:
                sugestao = (
                    f"O estoque de {item_nome} deve atingir o nível mínimo em aproximadamente "
                    f"{dias} dias."
                )

            else:
                sugestao = (
                    f"O estoque de {item_nome} não deve atingir o nível mínimo nos próximos "
                    f"{dias} dias previstos. Estoque considerado seguro."
                )

            sugestoes[item_nome] = sugestao

        except Exception as e:
            sugestoes[item_nome] = f"Erro ao gerar sugestão para {item_nome}: {str(e)}"


    previsoes_json = json.dumps(previsoes_todos_itens)
    sugestoes_json = json.dumps(sugestoes)

    context = {
        'nomes_itens': nomes_itens,
        'previsoes_json': previsoes_json,
        'sugestoes_json': sugestoes_json,
    }

    return render(request, 'analise/previsao.html', context)
