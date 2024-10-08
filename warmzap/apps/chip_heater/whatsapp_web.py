import os
import shutil
from dataclasses import dataclass
from datetime import timedelta
from time import sleep
from urllib.parse import quote

from django.utils import timezone
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class LoginQRCode:
    b64_qrcode: str
    directory_token: str


class WhatsAppWeb:
    _URL = 'https://web.whatsapp.com'

    _SELECTORS = {
        'mainPage': '#app > div > div.two._aigs',
    }

    def __init__(self, profile: str, autoconnect=True) -> None:
        self._profile = Options()
        self._profile.add_argument(f'user-data-dir={profile}')
        self._profile.add_argument('--no-sandbox')
        self._profile.add_argument('disable-dev-shm-usage')
        # self._profile.add_argument('--headless=new')
        # self._profile.add_argument("--window-size=1920,1080")
        service = Service()
        self.driver = webdriver.Chrome(self._profile, service)
        # self.driver.minimize_window()
        self.driver.set_script_timeout(500)
        self.driver.implicitly_wait(10)

        if autoconnect:
            self.connect()

    def connect(self):
        self.driver.get(self._URL)

    def wait_for_login(self, timeout=90):
        """Waits for the QR to go away"""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                self._SELECTORS['mainPage'],
            ))
        )

    def generate_login_qrcode(self, directory_token, profile_dir_path):
        self.directory_token = directory_token
        self.profile_dir_path = profile_dir_path

        # def get_canvas():
        #     while True:
        #         try:
        #             canvas = self.driver.find_element(
        #                 By.XPATH,
        #                 '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas',
        #             )
        #             return canvas
        #         except NoSuchElementException:
        #             pass

        try:
            canvas = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas',
                ))
            )
        except TimeoutException:
            yield True, 'Ocorreu um erro, tente novamente'
            return

        b64_qrcode = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas
        )

        yield False, LoginQRCode(b64_qrcode, self.directory_token)

        start_datetime = timezone.now()

        while start_datetime + timedelta(seconds=50) > timezone.now():
            number = self.driver.execute_script(
                "return localStorage.getItem('last-wid-md');"
            )
            if number:
                yield False, None
                self.wait_for_login(60)
                self.driver.quit()
                self.clean_browser_profile(self.profile_dir_path)
                yield number.split(':')[0][1:]
                return

        self.driver.quit()
        shutil.rmtree(self.profile_dir_path)
        yield True, 'QRcode expirado, tente novamente.'

    @classmethod
    def delete_unnecessary_in_default(cls, directory):
        folders_to_keep = [
            'IndexedDB',
            'Local Storage',
            'Sessions',
            'Session Storage',
        ]

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if item not in folders_to_keep and os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif os.path.isfile(item_path):
                os.remove(item_path)

        wpp_index_db_path = os.path.join(
            directory, 'IndexedDB/https_web.whatsapp.com_0.indexeddb.leveldb'
        )
        for item in os.listdir(wpp_index_db_path):
            item_path = os.path.join(wpp_index_db_path, item)
            if os.path.isfile(item_path) and (
                item.endswith('.log') or item in {'LOCK', 'LOG', 'LOG.old'}
            ):
                os.remove(item_path)

    @classmethod
    def clean_browser_profile(cls, directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if item == 'Default':
                cls.delete_unnecessary_in_default(
                    os.path.join(directory, 'Default')
                )
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

    @property
    def is_logged_in(self):
        """Returns if user is logged. Can be used if non-block needed for wait_for_login"""

        return 'class="two _aigs"' in self.driver.page_source

    def open_chat(self, number: str, message: str):
        self.connect()
        self.wait_for_login()
        sleep(6)
        url = f'{self._URL}/send?phone={number}&text={quote(message)}'
        self.driver.get(url)
        self.wait_for_login()

    def send_message_to_number(self, number: str, message: str):
        self.open_chat(number, message)

        send_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                '#main [data-testid="send"], #main [data-icon="send"]',
            ))
        )
        send_button.click()
        sleep(6)
