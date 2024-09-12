import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Use o mesmo perfil de usuário do Chrome
chrome_options = Options()
pasta = 'perfil'
chrome_options.add_argument(f'user-data-dir={pasta}')

# Inicie o WebDriver com o perfil de usuário
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acesse o WhatsApp Web
driver.get('https://web.whatsapp.com/')
input()
numero = driver.execute_script("return localStorage.getItem('last-wid-md');")

print(numero)
driver.quit()


# A sessão será restaurada automaticamente se o perfil contiver os dados corretos


def apagar_desnecessarios_em_default(diretorio):
    pastas_para_manter = [
        'IndexedDB',
        'Local Storage',
        'Sessions',
        'Session Storage',
    ]

    for item in os.listdir(diretorio):
        caminho_item = os.path.join(diretorio, item)
        if item not in pastas_para_manter and os.path.isdir(caminho_item):
            shutil.rmtree(caminho_item)  # Apaga pastas e subpastas
        elif os.path.isfile(caminho_item):
            os.remove(caminho_item)  # Apaga arquivos
    wpp_index_db_path = os.path.join(
        diretorio, 'IndexedDB/https_web.whatsapp.com_0.indexeddb.leveldb'
    )
    for item in os.listdir(wpp_index_db_path):
        item_path = os.path.join(wpp_index_db_path, item)

        if os.path.isfile(item_path):
            if item.endswith('.log') or item in {'LOCK', 'LOG', 'LOG.old'}:
                os.remove(item_path)


def apagar_tudo_exceto_default(diretorio):
    for item in os.listdir(diretorio):
        caminho_item = os.path.join(diretorio, item)
        if item == 'Default':  # Evita apagar a pasta 'Default'
            apagar_desnecessarios_em_default(
                os.path.join(diretorio, 'Default')
            )
        elif os.path.isdir(caminho_item):
            shutil.rmtree(caminho_item)  # Apaga pastas e subpastas
        else:
            os.remove(caminho_item)  # Apaga arquivos


apagar_tudo_exceto_default(pasta)
