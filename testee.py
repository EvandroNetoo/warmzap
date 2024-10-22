from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

options = Options()
options.add_argument('--headless=new')
service = Service()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://web.whatsapp.com/')
driver.quit()
