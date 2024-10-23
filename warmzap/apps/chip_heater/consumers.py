import asyncio
import json
import os
import shutil
from datetime import datetime, timedelta
from secrets import token_hex

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files import File
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from chip_heater.models import Chip
from chip_heater.whatsapp_web import WhatsAppWeb


class QRCodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.chip_name = data.get('chip_name')
        try:
            await self.run_qrcode_process()
        finally:
            await self.cleanup_resources()
        try:
            await self.close()
        except Exception:
            await self.cleanup_resources()

    async def disconnect(self, code):
        await self.cleanup_resources()

    async def run_qrcode_process(self):
        self.setup_selenium()
        await self.access_whatsapp_web()

        canvas = await self.get_qrcode_canvas()

        if not canvas:
            await self.notify_error(
                'Ocorreu um erro ao gerar o QR code, se persistir contate um administrador.'
            )
            return

        b64_qrcode = self.extract_qrcode(canvas)
        await self.send_qrcode(b64_qrcode)

        number = await self.wait_for_number_in_local_storage()

        if not number:
            await self.notify_error(
                'QRcode expirado, tente novamente, se persistir contate um administrador.'
            )
            return

        await self.check_login_status()
        await self.sync_data(number)

    def setup_selenium(self):
        self.profile_dir_path = f'wpp_sessions/{token_hex(16)}'
        options = Options()
        options.add_argument(f'user-data-dir={self.profile_dir_path}')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless=new')
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)

    async def access_whatsapp_web(self):
        self.driver.get('https://web.whatsapp.com/')

    async def get_qrcode_canvas(self) -> WebElement:
        timeout = 20
        end = datetime.now() + timedelta(seconds=timeout)
        while datetime.now() < end:
            try:
                canvas = self.driver.find_element(
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas',
                )
                return canvas
            except NoSuchElementException:
                await asyncio.sleep(0.5)
        return None

    def extract_qrcode(self, canvas: WebElement) -> str:
        return self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(22);", canvas
        )

    async def send_qrcode(self, b64_qrcode: str):
        await self.send(text_data=json.dumps({'qrcode': b64_qrcode}))

    async def wait_for_number_in_local_storage(self) -> str:
        timeout = 60
        end = datetime.now() + timedelta(seconds=timeout)
        number = self.driver.execute_script(
            "return localStorage.getItem('last-wid-md');"
        )
        now = datetime.now()

        while now < end and not number:
            number = self.driver.execute_script(
                "return localStorage.getItem('last-wid-md');"
            )
            now = datetime.now()
            await asyncio.sleep(0.5)

        return number.split(':')[0][1:] if number else None

    async def sync_data(self, number: str):
        chip_instance = Chip(
            name=self.chip_name, number=number, user=self.user
        )
        WhatsAppWeb.clean_browser_profile(self.profile_dir_path)
        zip_file = shutil.make_archive(
            self.profile_dir_path, 'zip', self.profile_dir_path
        )

        with open(zip_file, 'rb') as f:
            chip_instance.browser_profile = File(
                f, name=os.path.basename(zip_file)
            )
            await chip_instance.asave()

        os.remove(zip_file)
        shutil.rmtree(self.profile_dir_path)

    async def check_login_status(self):
        await self.send(
            text_data=json.dumps({'message': 'Sincronizando dados...'})
        )

        timeout = 90
        end = datetime.now() + timedelta(seconds=timeout)
        now = datetime.now()
        logged_in = 'two _aigs' in self.driver.page_source

        while not logged_in and now < end:
            logged_in = 'two _aigs' in self.driver.page_source
            await asyncio.sleep(0.5)

        if not logged_in:
            await self.notify_error(
                'Erro ao logar, tente novamente, se persistir contate um administrador.'
            )
        else:
            await self.send(text_data=json.dumps({'logged_in': True}))

        self.driver.quit()

    async def notify_error(self, message: str):
        await self.send(text_data=json.dumps({'message': message}))

    async def cleanup_resources(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        if hasattr(self, 'profile_dir_path'):
            try:
                shutil.rmtree(self.profile_dir_path)
            except FileNotFoundError:
                ...
