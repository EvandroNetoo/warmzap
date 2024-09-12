import shutil
from dataclasses import dataclass
from datetime import timedelta
from secrets import token_hex
from time import sleep

from core.settings import BASE_DIR
from django.utils import timezone
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import shutil


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
        profile_dir_path = BASE_DIR / f'wpp_sessions/{self.directory_token}'

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
            number = self.driver.execute_script(
                "return localStorage.getItem('last-wid-md');"
            )
            if number:
                yield False, number.split(':')[0][1:]
                sleep(15)
                self.driver.quit()
                return

        self.driver.quit()
        shutil.rmtree(profile_dir_path)
        yield True, 'QRcode expirado, tente novamente.'
        self.clean_browser_profile(profile_dir_path)

    def delete_unnecessary_in_default(self, directory):
        folders_to_keep = [
            'IndexedDB',
            'Local Storage',
            'Sessions',
            'Session Storage',
        ]

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if item not in folders_to_keep and os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Deletes folders and subfolders
            elif os.path.isfile(item_path):
                os.remove(item_path)  # Deletes files
        wpp_index_db_path = os.path.join(
            directory, 'IndexedDB/https_web.whatsapp.com_0.indexeddb.leveldb'
        )
        for item in os.listdir(wpp_index_db_path):
            item_path = os.path.join(wpp_index_db_path, item)

            if os.path.isfile(item_path):
                if item.endswith('.log') or item in {'LOCK', 'LOG', 'LOG.old'}:
                    os.remove(item_path)


    def clean_browser_profile(self, directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if item == 'Default':  # Avoids deleting the 'Default' folder
                self.delete_unnecessary_in_default(
                    os.path.join(directory, 'Default')
                )
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Deletes folders and subfolders
            else:
                os.remove(item_path)  # Deletes files
