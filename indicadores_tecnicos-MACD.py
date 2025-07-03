# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 18:58:35 2025
indicadores técnicos - MACD
@author: Cintia Perrone

Para ver como é feito o script do macd é necessário acessar o site do tradeview. Lá mostra como é feito o 
cálculo para apresentar no gráfico

MACD: https://br.tradingview.com/scripts/macd/
EMA: https://br.tradingview.com/scripts/ema/

"""

import yfinance as yf

# Ações que serem utilizadas nas análises
acoes = ["VALE", "PBR", "AMZN", "GOOG", "MSFT"]

# iniciando dicionário
ohlcv_data = {}

# Loop para cada ação
for acao in acoes:
    #temp = yf.download(acao,period="1mo", interval="15m",auto_adjust=(False))["Adj Close"]
    temp = yf.download(acao,period="1mo", interval="15m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[acao] = temp


   
# Criando função do MACD
def MACD(DF, mrapida=12, mlenta=26, msinal=9):
    # irá fazer a cópia da base
    df = DF.copy()
    df["ma_rapida"] = df["Close"].ewm(span=mrapida, min_periods=mrapida).mean()     
    df["ma_lenta"] = df["Close"].ewm(span=mlenta, min_periods=mlenta).mean() 
    df["macd"] = df["ma_rapida"] - df["ma_lenta"]
    df["sinal"] = df["macd"].ewm(span=msinal, min_periods=msinal).mean()
    return df.loc[:,["macd","sinal"]] # irá retornar todas as linhas e as colunas macd e sinal


# Loop para cada ação do dicionário
for acao in ohlcv_data:
    ohlcv_data[acao][["MACD","SINAL"]] = MACD(ohlcv_data[acao])# irá criar 2 colunas e irá chamar a função MACD