from dataclasses import dataclass
from datetime import timedelta
import shutil
from time import sleep
from typing import Generator
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from secrets import token_hex

from core.settings import BASE_DIR
from django.utils  import timezone
@dataclass
class LoginQRcode:
    b64_qrcode: str
    directory_token: str

class WhatsappWeb:
    def __init__(self):
        self.driver = None
        self.directory_token = None

    def generate_login_qrcode(self):
        self.directory_token = token_hex(16)
        profile_dir_path= BASE_DIR / f"wpp_sessions/{self.directory_token}"

        chrome_options = Options()
        chrome_options.add_argument(f'user-data-dir={profile_dir_path}')
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        self.driver.get('https://web.whatsapp.com/')

        def get_canvas():
            while True:
                try:
                    canvas = self.driver.find_element(
                        By.XPATH,
                        '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas',
                    )
                    return canvas
                except NoSuchElementException:
                    pass

        canvas = get_canvas()
        b64_qrcode = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas
        )

        yield False, LoginQRcode(b64_qrcode, self.directory_token)

        start_datetime = timezone.now()
        
        while start_datetime + timedelta(seconds=50) > timezone.now():
            number = self.driver.execute_script("return localStorage.getItem('last-wid-md');")
            if number:
                yield False, number.split(':')[0][1:]
                sleep(15)
                self.driver.quit()
                return

        self.driver.quit()
        shutil.rmtree(profile_dir_path)
        yield True, 'QRcode expirado, tente novamente.'

        