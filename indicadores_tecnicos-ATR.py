# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 20:42:38 2025
@author: Cintia Perrone

Indicadores Técnicos -  ATR

Para ver como é feito o script do ATR é necessário acessar o site do tradeview. Lá mostra como é feito o 
cálculo para apresentar no gráfico

ATR: https://br.tradingview.com/scripts/atr/  -> usar média de 9 e SMA

"""
# importando bibliotecas
import yfinance as yf

# ações a ser analisadas
acoes = ["AMZN", "MSFT", "GOOG", "VALE"]

# inicializando dicionário
ohclv_data = {}

# loop e inserindo no dicionário
for acao in acoes:
    print(acao)
    temp = yf.download(acao,period="1mo",interval="5m")
    temp.dropna(how="any", inplace=True) # atualiza a tabela virtual
    ohclv_data[acao] = temp # insere as informações da tabela virtual no dicionário
    

# Para ver se funciona para um único exemplo
# df = ohclv_data["VALE"]    
   
# Criando função ATR
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

# iniciando o loop utilizando a função ATR
for acoes in ohclv_data:
    print(acoes)
    ohclv_data[acoes]["ATR"] = ATR(ohclv_data[acoes]) # o ohclv_data[acao] = DF caso queira mudar o período basta colocar  ohclv_data[acao]["ATR"] = ATR(ohclv_data[acao],14)
    