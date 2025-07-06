# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 16:22:08 2025
indicadores técnicos - Renko

necessário instalar a biblioteca stocktrends
@author: perro
"""

# Importando as bibliotecas necessárias
import yfinance as yf
from stocktrends import Renko
import pandas as pd

#Ações a serem analisadas
acoes = ["BTC-USD"]

# inicializando dicionário de ações
ohlcv_data = {}

# inicializando dicionário de hora e data
hora_data = {}

# inicializando dicionário renko_data
renko_data={}

# Loop para carregar os dados nos dicionários de ações e hora/data
for acao in acoes:
    temp = yf.download(acao,period="1mo", interval="5m")
    temp.dropna(how="any", inplace=True)
    ohlcv_data[acao] = temp
    
    temp = yf.download(acao,period="1y",interval="1h")
    temp.dropna(how="any", inplace=True)
    hora_data[acao] = temp
    
# Criando a função ATR
def ATR(DF, n=14):
    df=DF.copy() # irá fazer a cópia da base de dados para não alterar a base anterior
    df["H-L"] = df["High"] - df["Low"]
    df["H-PF"] = df["High"] - df["Close"].shift(1) # joga o valor para o próximo dia
    df["L-PF"] = df["Low"] - df["Close"].shift(1) # joga o valor para o próximo dia
    df["TR"] = df[["H-L", "H-PF", "L-PF"]].max(axis=1, skipna=False)
    # TR = True range; max(axis=1) aqui calcula o valor máx da linha, skipna=False não irá pular as linhas com na
    # irá calcular o ATR
   
    # span é utilizado no tradeview
    #df["ATR"] = df["TR"].ewm(span=n,min_periods=n).mean() # irá calcular a média móvel de 14 períodos
    
    # com é utilizado no yahoo finance
    df["ATR"] = df["TR"].ewm(com=n,min_periods=n).mean() # irá calcular a média móvel de 14 períodos
    return df["ATR"]

#df = ohlcv_data["BTC-USD"]

# Criando função Renko
def renko_DF (DF, hora_df):
    df = DF.copy()
    # irá deletar a coluna
    #df.drop("High", axis=1, inplace=True) # Preciso colocar axis = 1 para encontrar a coluna
    
    # Preciso fazer com o que a coluna datetime se torne uma coluna
    df.reset_index(inplace=True)
    
    # Preciso mudar o nome da coluna, pq a função só aceita coluna com letra minúscula
    df.columns = ["date", "open", "high", "low", "close", "volume"]
    
    # Associando a tabela à função Renko
    df2 = Renko(df)
    df2.brick_size = 3 * round(ATR(hora_df, 120).iloc[-1], 0)
    renko_df = df2.get_ohlc_data()
    renko_df["esta_em_tendencia"] = renko_df["uptrend"].map({True: "sim",False: "não"})
    renko_df.drop("uptrend", axis = 1, inplace=True)
    return renko_df

for acoes in ohlcv_data:
    renko_data[acoes] = renko_DF(ohlcv_data[acoes], hora_data[acoes])
