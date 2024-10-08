import os
import shutil
from dataclasses import dataclass
from time import sleep
from urllib.parse import quote

from selenium import webdriver
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
