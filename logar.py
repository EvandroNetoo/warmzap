import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

pasta = 'perfil'

chrome_options = Options()
chrome_options.add_argument(f'user-data-dir={pasta}')

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://web.whatsapp.com/')

input('Pressione Enter depois de escanear o QR Code e estar logado...')

driver.quit()


def apagar_tudo_exceto_default(diretorio):
    for item in os.listdir(diretorio):
        caminho_item = os.path.join(diretorio, item)
        if item != 'Default':  # Evita apagar a pasta 'Default'
            if os.path.isdir(caminho_item):
                shutil.rmtree(caminho_item)  # Apaga pastas e subpastas
            else:
                os.remove(caminho_item)  # Apaga arquivos


apagar_tudo_exceto_default(pasta)
