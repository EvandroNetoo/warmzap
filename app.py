import base64
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Configure o WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Opcional, se você não precisar ver o navegador
chrome_options.add_argument("incognito")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://web.whatsapp.com/')

def get_canvas():
    while True:
        try:
            canvas = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')
            return canvas
        except NoSuchElementException:
            pass

canvas = get_canvas()
canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
