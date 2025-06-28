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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Caminho onde está instalado chrome
caminho_servico = Service(r"C:\\Users\\perro\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

# injetar argumentos para desabilitar comando
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=caminho_servico, options=options)

#  Ele burla o campo de verificação e apresenta o site
driver.get("https://charts.bitbo.io/pi-cycle-top/")
