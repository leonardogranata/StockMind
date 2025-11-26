import pandas as pd
from prophet import Prophet
from .models import Consumo

def prever_consumo(item_nome, dias=15):
    # Pega dados direto do banco; sem arquivo temporário
    qs = (
        Consumo.objects
        .filter(item__nome=item_nome)
        .order_by('data')
        .values('data', 'quantidade')
    )
    df = pd.DataFrame(list(qs))

    # Se não existe coluna 'data' ou 'quantidade' ou está vazio
    if df.empty or len(df) < 2:
        print(f"AVISO: Dados insuficientes para prever o item {item_nome}. Necessário no mínimo 2 registros.")
        return None

    # Renomeia e formata
    df = df.rename(columns={'data': 'ds', 'quantidade': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], errors='coerce')

    # Remove linhas com ds inválido
    df = df.dropna(subset=['ds'])
    if df.empty or len(df) < 2:
        print(f"AVISO: Após limpeza, dados insuficientes para {item_nome}.")
        return None

    df['floor'] = 0

    modelo = Prophet()
    modelo.fit(df)

    futuro = modelo.make_future_dataframe(periods=dias)
    futuro['floor'] = 0

    previsao = modelo.predict(futuro)
    return previsao[['ds', 'yhat']].tail(dias)
