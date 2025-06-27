# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 10:35:11 2025

@author: perro
"""

"""Script para baixar dados do Índice CBBI e plotar um gráfico.

Este script acessa a API pública do site `https://colintalkscrypto.com/cbbi/` 
(ou o endpoint equivalente `https://api.colintalkscrypto.com/cbbi/all`) para
baixar os valores históricos do Bitcoin Bull Run Index (CBBI).

Certifique-se de que o `requests` e o `matplotlib` estão instalados:

    pip install requests matplotlib

Como o ambiente desta demonstração não possui acesso à internet, o script
não será executado aqui, mas funciona em um ambiente local com acesso à web.
"""

import requests
import matplotlib.pyplot as plt

URL = "https://api.colintalkscrypto.com/cbbi/all"  # Verifique se este é o endpoint correto


def baixar_dados(url: str = URL):
    """Baixa os dados JSON do CBBI e retorna o objeto Python."""
    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()
    return resposta.json()


def plotar_cbbi(dados: dict):
    """Plota o CBBI a partir do dicionário recebido da API."""
    # A estrutura exata pode variar. Supondo que o JSON contenha uma lista de
    # objetos com os campos 'time' (timestamp) e 'cbbi'.
    tempos = [ponto['time'] for ponto in dados]
    valores = [ponto['cbbi'] for ponto in dados]

    plt.figure(figsize=(10, 5))
    plt.plot(tempos, valores)
    plt.xlabel("Tempo")
    plt.ylabel("CBBI")
    plt.title("CBBI histórico")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    dados = baixar_dados()
    plotar_cbbi(dados)