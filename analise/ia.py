import pandas as pd
from prophet import Prophet
from .models import Consumo

def gerar_csv_consumo(item_nome):
    dados = (
        Consumo.objects
        .filter(item__nome=item_nome)
        .order_by('data')
        .values('data', 'quantidade')
    )
    df = pd.DataFrame(list(dados))
    df.to_csv('dados_consumo.csv', index=False)
    return 'dados_consumo.csv'

def prever_consumo(item_nome, dias=15):
    caminho = gerar_csv_consumo(item_nome)
    df = pd.read_csv(caminho)
    df = df.rename(columns={'data': 'ds', 'quantidade': 'y'})
    modelo = Prophet()
    modelo.fit(df)
    futuro = modelo.make_future_dataframe(periods=dias)
    previsao = modelo.predict(futuro)
    return previsao[['ds', 'yhat']].tail(dias)

