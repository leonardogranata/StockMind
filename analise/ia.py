import pandas as pd
from prophet import Prophet
from .models import Consumo

def gerar_csv_consumo(item_nome):
    dados = (
        Consumo.objects
        .filter(item__nome=item_nome)
        .order_by('data')
        .values('item', 'data', 'quantidade')
    )
    df = pd.DataFrame(list(dados))
    df.to_csv('dados_consumo.csv', index=False)
    return 'dados_consumo.csv'

def prever_consumo(item_nome, dias=15):
    caminho = gerar_csv_consumo(item_nome)

    try:
        df = pd.read_csv(caminho)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        print(f"AVISO: Sem dados válidos para o item {item_nome}")
        return None  # <── retorna None caso o CSV esteja vazio

    # Verificação mínima
    if df is None or df.empty or len(df) < 2:
        print(f"AVISO: Dados insuficientes para prever o item {item_nome}. Necessário no mínimo 2 registros.")
        return None

    df = df.rename(columns={'data': 'ds', 'quantidade': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    df['floor'] = 0
    
    modelo = Prophet()
    modelo.fit(df)
    
    futuro = modelo.make_future_dataframe(periods=dias)
    futuro['floor'] = 0
    
    previsao = modelo.predict(futuro)
    
    return previsao[['ds', 'yhat']].tail(dias)
