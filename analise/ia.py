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
    """
    Prevê o consumo de um item para os próximos 'dias',
    garantindo que a previsão não seja negativa.
    """
    caminho = gerar_csv_consumo(item_nome)
    
    try:
        df = pd.read_csv(caminho)
    except FileNotFoundError:
        print(f"AVISO: Arquivo CSV não encontrado para o item {item_nome}")
        # Retorna um DataFrame vazio se o arquivo não existir
        return pd.DataFrame(columns=['ds', 'yhat'])

    # 1. VERIFICAÇÃO DE SEGURANÇA: Prophet precisa de pelo menos 2 pontos de dados.
    if len(df) < 2:
        print(f"AVISO: Dados insuficientes para prever o item {item_nome}. Necessário no mínimo 2 registros.")
        # Retorna um DataFrame vazio se não houver dados suficientes
        return pd.DataFrame(columns=['ds', 'yhat'])

    df = df.rename(columns={'data': 'ds', 'quantidade': 'y'})
    
    # Garante que a coluna 'ds' seja do tipo datetime
    df['ds'] = pd.to_datetime(df['ds'])

    # 2. ADICIONA O PISO (FLOOR): Diz ao Prophet que a quantidade não pode ser menor que 0
    df['floor'] = 0
    
    modelo = Prophet()
    modelo.fit(df)
    
    futuro = modelo.make_future_dataframe(periods=dias)

    # 3. ADICIONA O PISO AO DATAFRAME FUTURO: Essencial para que a previsão respeite o limite
    futuro['floor'] = 0
    
    previsao = modelo.predict(futuro)
    
    # Retorna apenas os dias futuros da previsão com as colunas necessárias
    return previsao[['ds', 'yhat']].tail(dias)
