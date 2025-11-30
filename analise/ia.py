import pandas as pd
from prophet import Prophet
from .models import Consumo

def prever_consumo(item_nome, dias=15):
    # Busco no banco todos os registros de consumo desse item
    # Já ordenados por data, porque o Prophet precisa da série temporal organizada
    qs = (
        Consumo.objects
        .filter(item__nome=item_nome)
        .order_by('data')
        .values('data', 'quantidade')
    )
    df = pd.DataFrame(list(qs))

    # Se não tiver pelo menos 2 registros, não dá pra prever nada (o Prophet exige isso)
    if df.empty or len(df) < 2:
        print(f"AVISO: Dados insuficientes para prever o item {item_nome}. Necessário no mínimo 2 registros.")
        return None

    # Renomeio as colunas para o formato padrão do Prophet:
    # 'ds' = datas e 'y' = valores da série (consumo)
    df = df.rename(columns={'data': 'ds', 'quantidade': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], errors='coerce')

    # Tiro qualquer linha que tenha data inválida
    if df.empty or len(df) < 2:
        print(f"AVISO: Após limpeza, dados insuficientes para {item_nome}.")
        return None

    # 'floor' = valor mínimo permitido no modelo (não faz sentido ter consumo negativo)
    df['floor'] = 0

    # Crio o modelo Prophet com:
    # - sazonalidade semanal ativada (padrões por dia da semana)
    # - sensibilidade menor à tendência (changepoint_prior_scale baixo = crescimento mais suave)
    modelo = Prophet(
        weekly_seasonality=True,
        daily_seasonality=False,
        yearly_seasonality=False,
        changepoint_prior_scale=0.02  # deixo o modelo menos sensível a mudanças bruscas
    )

    # Adiciono manualmente a sazonalidade semanal com menor complexidade
    # (fourier menor = curva menos ondulada)
    modelo.add_seasonality(
        name='weekly',
        period=7,
        fourier_order=1,  # baixa variação semanal
        prior_scale=0.1   # sem exageros no efeito semanal
    )

    # Treino o modelo com os dados do item
    modelo.fit(df)

    # Gero um dataframe com as datas futuras que quero prever (15 dias por padrão)
    futuro = modelo.make_future_dataframe(periods=dias)
    futuro['floor'] = 0  # aplico o floor também no futuro

    # Faço a previsão e retorno só as colunas importantes:
    # 'ds' = data prevista e 'yhat' = valor previsto
    previsao = modelo.predict(futuro)
    return previsao[['ds', 'yhat']].tail(dias)
