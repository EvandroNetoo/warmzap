from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Use o mesmo perfil de usuário do Chrome
chrome_options = Options()
chrome_options.add_argument("user-data-dir=/home/evandro/python_projects/warmzap/perfil")

# Inicie o WebDriver com o perfil de usuário
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acesse o WhatsApp Web
driver.get('https://web.whatsapp.com/')

# A sessão será restaurada automaticamente se o perfil contiver os dados corretos
input()