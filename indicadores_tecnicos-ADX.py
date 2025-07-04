# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 10:59:16 2025
indicadores técnicos - ADX
Este indicador verifica de 0 a 100 o valor da força dentro de uma tendência conforme tabela abaixo:
    0-25: tendência fraca
    25-50: tendência forte
    50-75: tendência mto forte
    75-100: tendência extremamente forte (mto raro)
    
    Para ver como é feito o script do ADX é necessário acessar o site do tradeview. Lá mostra como é feito o 
    cálculo para apresentar no gráfico
    
Para calcular o ADX preciso calcular o TR, depois preciso calcular o movimento positivo e movimento negativo  
como utiliza o período de 14 dias, preciso fazer o mesmo cálculo para TR, movimento positivo e movimento negativo
depois disso preciso adicionar o indicador de direção positivo e negativo

ADX - BTC/RSI: https://br.tradingview.com/script/idvinAv2/
ADX: https://br.tradingview.com/script/AwoDGYNg-ADX-Trend-Visualizer-with-Dual-Thresholds/

Site de apoio: https://stackoverflow.com/questions/63020750/how-to-find-average-directional-movement-for-stocks-using-pandas
@author: Cintia Perrone
"""

# importando as bibliotecas
import yfinance as yf
import numpy as np
import pandas as pd

# Ações a serem analisadas
acoes = ["VALE", "BTC-USD"]

# Inicializando dicionário
ohlcv_data = {}

# Loop para carregar as ações para o dicionário
for acao in acoes:
    temp = yf.download(acao,period="6mo", interval="4h") # Período de 4 horas
    temp.dropna(how="any",inplace=True) # irá atualizar a tabela virtual
    ohlcv_data[acao] = temp
    
# Utilizando função do ATR
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

# Utilizando função do ADX
def ADX(DF,n=14):
    df= DF.copy() # irá fazer a cópia da base de dados
    
    # chama função do ATR
    df["ATR"] = ATR(df,n)
    
    df["subida"] = df["High"] - df["High"].shift(1) # Máx - Máx anterior
    df["descida"] = df["Low"] - df["Low"].shift(1) # Mín - Mín anterior
    
    #Irá verificar se está em movimento de subida, caso seja contrário irá retornar 0
    df["+dm"] = np.where((df["subida"] > df["descida"]) & (df["subida"] > 0),df["subida"], 0)

    #Irá verificar se está em movimento de descida, caso seja contrário irá retornar 0
    df["-dm"] = np.where((df["descida"] > df["subida"]) & (df["descida"] > 0),df["descida"], 0)
    
    # Calcula o valor do indicador de direção positivo
    df["+di"] = 100 * (df["+dm"]/df["ATR"]).ewm(span=n, min_periods=n).mean()
    
    # para yahoo finance - indicador positivo
    # df["+di"] = 100 * (df["+dm"]/df["ATR"]).ewm(com=n, min_periods=n).mean()
    
    # Calcula o valor do indicador de direção negativo
    df["-di"] = 100 * (df["-dm"]/df["ATR"]).ewm(span=n, min_periods=n).mean()
    
    # para yahoo finance - indicador negativo
    #df["-di"] = 100 * (df["-dm"]/df["ATR"]).ewm(com=n, min_periods=n).mean()
    
    #Calcula o valor de ADX baseado no valor absoludo de +di e -di baseado na média móvel exponencial
    df["ADX"] = 100 * abs((df["+di"]- df["-di"]) / (df["+di"] + df["-di"])).ewm(span=n, min_periods=n).mean()
    
    # Indica qual o nível da força da tendência:
    df["forca_tendencia"] = pd.cut(df["ADX"],bins=[0,25,50,75,100], right=False,labels=["fraca", "forte","mto forte","extremamente forte"])
    return df.loc[:,["ADX", "forca_tendencia"]]

for acoes in ohlcv_data:
    ohlcv_data[acoes][["ADX","forca_tendencia"]] = ADX(ohlcv_data[acoes],20)
