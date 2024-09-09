from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure o caminho para o perfil de usuário do Chrome
chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\2024122760105\Desktop\warmzap\perfil")

# Inicie o WebDriver com o perfil de usuário
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Acesse o WhatsApp Web
driver.get('https://web.whatsapp.com/')

# Aguarde o usuário escanear o QR Code e fazer login
input("Pressione Enter depois de escanear o QR Code e estar logado...")

# O perfil agora armazena os cookies e a sessão, então o login será mantido
driver.quit()

#cache