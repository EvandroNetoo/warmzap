import os
import re
import shutil
import zipfile
from pathlib import Path
from secrets import token_hex

import requests
from core.env_settings import env_settings
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from chip_heater.whatsapp_web import WhatsAppWeb


class Chip(models.Model):
    class StageChoices(models.TextChoices):
        NOT_STARTED = 'NT', 'Não iniciado'
        STARTED = 'ST', 'Em aquecimento'
        COMPLETED = 'CP', 'Concluído'
        BANNED = 'BN', 'Banido'

    user = models.ForeignKey(
        'accounts.user',
        models.CASCADE,
        related_name='chips',
        verbose_name='usuário',
    )

    name = models.CharField('nome', max_length=15, blank=True)
    number = models.CharField(
        'número',
        max_length=15,
    )
    browser_profile = models.FileField(
        'perfil do navegador',
        upload_to='browser_profiles',
        validators=[FileExtensionValidator(['zip'])],
    )
    stage = models.CharField(
        'Fase',
        max_length=2,
        choices=StageChoices.choices,
        default=StageChoices.NOT_STARTED,
    )

    days_to_heat = models.PositiveIntegerField(
        'dias para aquecer', null=True, blank=True
    )
    heated_days = models.PositiveIntegerField('dias aquecidos', default=0)

    class Meta:
        verbose_name = 'chip'
        verbose_name_plural = 'chips'

    def formated_number(self):
        number = self.number
        formatted = re.sub(
            r'(\d{2})(\d{2})(\d{5})(\d{4})', r'+\1 (\2) \3-\4', number
        )
        return formatted

    def send_message(self, to: str, message: str):
        Path(settings.BASE_DIR / 'wpp_sessions').mkdir(
            parents=True, exist_ok=True
        )

        directory_token = token_hex(16)
        profile_dir_path = (
            settings.BASE_DIR / f'wpp_sessions/{directory_token}'
        )
        zip_file_path = (
            settings.BASE_DIR / f'wpp_sessions/{directory_token}.zip'
        )

        try:
            download_url = f'{env_settings.HOST}{self.browser_profile.url}'

            response = requests.get(download_url, stream=True, timeout=60)
            response.raise_for_status()

            with open(zip_file_path, 'wb') as out_file:
                out_file.write(response.raw.data)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(profile_dir_path)

            WhatsAppWeb(profile_dir_path).send_message_to_number(to, message)

        finally:
            os.remove(zip_file_path)
            shutil.rmtree(profile_dir_path)


class Message(models.Model):
    message = models.TextField('mensagem')

    class Meta:
        verbose_name = 'mensagem'
        verbose_name_plural = 'mensagens'

    def __str__(self) -> str:
        return self.message[:50]
