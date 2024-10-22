from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument('--headless=new')
service = Service()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://web.whatsapp.com/')
driver.quit()
