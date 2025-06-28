# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:23:12 2025

@author: Cintia Perrone
"""

"""
from selenium import webdriver

options = webdriver.ChromeOptions() 
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options, executable_path=r'C:\\Users\\perro\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
driver.get("https://charts.bitbo.io/pi-cycle-top/")

"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Caminho onde está instalado o executável chrome
caminho_servico = Service(
    r"C:\Users\perro\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
)
# injetar argumentos para desabilitar comando
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

#  Ele burla o campo de verificação e apresenta o site
driver = webdriver.Chrome(service=caminho_servico, options=options)

#Try e finally finaliza a sessão caso dê algum problema na execução do script
try: 
    driver.get("https://charts.bitbo.io/pi-cycle-top/")
    
    # Aguarda alguns segundos para garantir que o gráfico foi carregado
    import time
    # aguarda 60 segundos 
    time.sleep(60)
    
    
    # Ajusta o print para pegar a tela toda
    altura = driver.execute_script("return document.body.parentNode.scrollHeight")
    largura = driver.execute_script("return document.body.parentNode.scrollWidth")
    driver.set_window_size(largura, altura)
    
    # Salva a imagem no diretório onde o script está salvo
    driver.save_screenshot("pi_cycle_top.png")

finally:  
    driver.quit()
