# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 16:51:57 2025
@author: Cintia Perrone

Indicadores Técnicos -  IFR ou RSI

Para ver como é feito o script do RSI é necessário acessar o site do tradeview. Lá mostra como é feito o 
cálculo para apresentar no gráfico

RSI: https://br.tradingview.com/scripts/stochasticrsi/  -> vai de 0 a 100, > 70 é sobrecomprado e < 30 é
sobrevendido

Site de apoio: https://blog.quantinsti.com/rsi-indicator/
"""

# Importando as bibliotecas
import yfinance as yf
import numpy as np

# Ações a serem analisadas
acoes = ["BTC-USD", "VALE"]

# Inicializando dicionário
ohclv_data = {}

# Loop para alimentar o dicionário
for acao in acoes:
    print(acao)
    temp = yf.download(acao,period="6mo", interval="1d") # irá pegar o período de 6 meses do gráfico diário
    temp.dropna(how="any", inplace=True) # irá excluir todos os valores com na
    ohclv_data[acao] = temp # irá alimentar o dicionário
     
# df = ohclv_data["VALE"]  
# n= 14    
# Irá criar a função RSI

def RSI (DF, n=14): # DF = acao, n=14 período a ser analisado
    df = DF.copy() # fará cópia da base de dados
    df["change"] = df["Close"] - df["Close"].shift(1) # fará a != de 1 dia - o anterior
    df["ganho"] = np.where(df["change"]>=0,df["change"],0)
    df["perda"] = np.where(df["change"]<0,-1*df["change"],0)
    df["mediaganho"] = df["ganho"].ewm(alpha=1/n, min_periods=n).mean() # preciso da média de ganhos
    df["mediaperda"] = df["perda"].ewm(alpha=1/n, min_periods=n).mean()  # preciso da média de perdas
    df["rs"] = df["mediaganho"]/df["mediaperda"]
    df["rsi"] = 100 - (100/(1+df["rs"])) # aqui consigo chegar no valor do RSI
    return df["rsi"]

# Inicia o loop de verificação para cada ação
for acoes in ohclv_data:
    ohclv_data[acoes]["RSI"] = RSI(ohclv_data[acoes])
