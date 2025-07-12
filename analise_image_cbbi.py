# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 15:59:36 2025

@author: LngUser
""""""Script para baixar dados do Índice CBBI e plotar um gráfico.

Este script acessa a API pública do site `https://colintalkscrypto.com/cbbi/`
(ou o endpoint equivalente `https://api.colintalkscrypto.com/cbbi/all`) para
baixar os valores históricos do Bitcoin Bull Run Index (CBBI).

Certifique-se de que o `requests` e o `matplotlib` estão instalados:

    pip install requests matplotlib

Como o ambiente desta demonstração não possui acesso à internet, o script
não será executado aqui, mas funciona em um ambiente local com acesso à web.

Instruções para analisar uma imagem e transformá-la em tabela
------------------------------------------------------------
1. Instale as dependências de OCR e manipulação de imagem:

       pip install pillow pytesseract pandas

2. Utilize a função ``imagem_para_tabela`` deste módulo informando o caminho
   da imagem que contém a tabela. Ela utiliza ``pytesseract`` para extrair o
   texto e tenta organizar o resultado em um ``pandas.DataFrame``.
"""
# Instalando bibliotecas
import requests
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import pytesseract

# Função para baixar os dados de CBBI
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
    
def imagem_para_tabela(caminho_imagem: str) -> pd.DataFrame:
    """Converte uma imagem contendo uma tabela em um DataFrame.

    A função utiliza ``pytesseract`` para realizar OCR na imagem. O texto
    extraído é separado por linhas e cada linha é dividida em colunas com
    ``split()``. Em imagens muito complexas pode ser necessário um tratamento
    adicional para identificar as colunas corretamente.
    """
    imagem = Image.open(caminho_imagem)
    texto = pytesseract.image_to_string(imagem, lang="por")
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    dados = [linha.split() for linha in linhas]
    return pd.DataFrame(dados)    

if __name__ == "__main__":
    dados = baixar_dados()
    plotar_cbbi(dados)