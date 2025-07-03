# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 11:49:20 2025
@author: Cintia Perrone

Indicadores Técnicos -  Bandas de Bollinger

Para ver como é feito o script das bandas de bollinger  é necessário acessar o site do tradeview. Lá mostra como é feito o 
cálculo para apresentar no gráfico

BB: https://br.tradingview.com/scripts/bollingerbands/  -> usar média 20

Site de apoio: https://quantbrasil.com.br/blog/como-calcular-as-bandas-de-bollinger-em-python/

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
# n=20   
   
# Criando função ATR
def BandaBollinger(DF, n= 20,fator_deslocamento=2): #n = período e k = fator de deslocamento da banda
    df = DF.copy() # Fazendo a cópia da base de dados
    df["DP"] = df["Close"].rolling(n).std() # Calcula o desvio padrão
    df["BM"] = df["Close"].rolling(n).mean()  # Banda do meio; irá rolar e calcular a média dos períodos de n
    df["BC"] = df["BM"] + df["DP"] * fator_deslocamento # banda de cima
    df["BB"] = df["BM"] - df["DP"] * fator_deslocamento # banda de baixo
    return df[["BM","BC","BB"]] # irá apresentar estas colunas na tabela

for acoes in ohclv_data:
    print(acoes)
    ohclv_data[acoes][["BC","BM","BB"]] = BandaBollinger(ohclv_data[acoes]) # média de 20 n preciso colocar, pq já está implicíto na função
    # irá acrescentar as colunas BM, BC, BB