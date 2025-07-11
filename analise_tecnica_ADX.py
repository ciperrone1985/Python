# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 17:13:43 2025
Usando ADX na biblioteca ta

@author: perro
"""

# Importando biblioteca
from ta.trend import ADXIndicator # utiliza ADX
import yfinance as yf

# Ações a serem analisadas
acoes = ["BTC-USD"]

# Carrega informações a partir do yfinance
df = yf.download(acoes,period="1y", interval="4h")

# Transformando os dados no formato que o ADX precisa receber
high_series  = df["High"].squeeze()   # de (N×1) DataFrame para (N,) Series
low_series   = df["Low"].squeeze()
close_series = df["Close"].squeeze()

# Limpando os valores em branco
high_series  = high_series.dropna()
low_series   = low_series.dropna()
close_series = close_series.dropna()

# Adionando informações do indicador ADX
ind_adx = ADXIndicator(high = high_series, low= low_series, close = close_series, window=14, fillna=False)

# Adiciona informações no DataFrame
df["ADX"] = ind_adx.adx()
df["+DI"] = ind_adx.adx_pos()
df["-DI"] = ind_adx.adx_neg()

print(df[["High","Low","Close","ADX","+DI","-DI"]].tail())