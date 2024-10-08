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

    async def disconnect(self, close_code):
        if hasattr(self, 'driver'):
            self.driver.quit()
        if hasattr(self, 'profile_dir_path'):
            try:
                shutil.rmtree(self.profile_dir_path)
            except FileNotFoundError:
                ...

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.chip_name = data.get('chip_name')

        await self.run_qrcode_process()
        await self.close()

    async def run_qrcode_process(self):

        # Configuração do Selenium com opções e serviço
        self.profile_dir_path = f'wpp_sessions/{token_hex(16)}'
        options = Options()
        options.add_argument(f'user-data-dir={self.profile_dir_path}')
        options.add_argument('--no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        service = Service()

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_script_timeout(500)
        self.driver.implicitly_wait(10)

        # Acesse o WhatsApp Web
        self.driver.get('https://web.whatsapp.com/')

        async def get_canvas() -> WebElement:
            timeout = 20  # Timeout de 20 segundos
            end = datetime.now() + timedelta(seconds=timeout)
            while datetime.now() < end:
                try:
                    # Tenta encontrar o elemento do QR code
                    canvas = self.driver.find_element(
                        By.XPATH,
                        '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas',
                    )
                    return canvas
                except NoSuchElementException:
                    await asyncio.sleep(0.5)
            return None

        # Busca o elemento canvas
        canvas = await get_canvas()

        if not canvas:
            await self.send(
                text_data=json.dumps({
                    'message': 'Ocorreu um erro ao gerar o QR code, se persistir contate um administrador.'
                })
            )
            return

        # Executa o script para extrair o QR code em base64
        b64_qrcode = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(22);", canvas
        )

        # Envia o QR code para o cliente via WebSocket
        await self.send(
            text_data=json.dumps({
                'qrcode': b64_qrcode,
            })
        )

        # Verifica o número no localStorage (aguarda por 60 segundos)
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

        if not number:
            await self.send(
                text_data=json.dumps({
                    'message': 'QRcode expirado, tente novamente, se persistir contate um administrador.'
                })
            )
            return

        # Se o número for encontrado, remove o sufixo '@'
        number = number.split('@')[0]
        await self.send(
            text_data=json.dumps({'message': 'Sincronizando dados...'})
        )

        # Verifica se o usuário está logado
        timeout = 90
        end = datetime.now() + timedelta(seconds=timeout)
        now = datetime.now()
        logged_in = 'class="two _aigs"' in self.driver.page_source
        while not logged_in and now < end:
            logged_in = 'class="two _aigs"' in self.driver.page_source
            await asyncio.sleep(0.5)

        if not logged_in:
            await self.send(
                text_data=json.dumps({
                    'message': 'Erro ao logar, tente novamente, se persistir contate um administrador.'
                })
            )
            return

        self.driver.quit()

        chip_instance = Chip(
            name=self.chip_name,
            number=number,
            user=self.user,
        )
        WhatsAppWeb.clean_browser_profile(self.profile_dir_path)
        zip_file = shutil.make_archive(
            self.profile_dir_path,
            'zip',
            self.profile_dir_path,
        )
        with open(zip_file, 'rb') as f:
            chip_instance.browser_profile = File(
                f, name=os.path.basename(zip_file)
            )
            await chip_instance.asave()

        os.remove(zip_file)
        shutil.rmtree(self.profile_dir_path)

        # Notifica o cliente que o login foi concluído
        await self.send(text_data=json.dumps({'logged_in': True}))
