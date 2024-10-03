import re
import shutil
import zipfile
from secrets import token_hex

from accounts.models import User
from django.conf import settings
from django.core.files.storage import default_storage
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
        User,
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
        directory_token = token_hex(16)
        profile_dir_path = (
            settings.BASE_DIR / f'wpp_sessions/{directory_token}'
        )
        try:
            with default_storage.open(self.browser_profile.path, 'rb') as f:
                with zipfile.ZipFile(f, 'r') as zip_ref:
                    zip_ref.extractall(profile_dir_path)

                WhatsAppWeb(profile_dir_path).send_message_to_number(
                    to, message
                )
        finally:
            shutil.rmtree(profile_dir_path)


class Message(models.Model):
    message = models.TextField('mensagem')

    class Meta:
        verbose_name = 'mensagem'
        verbose_name_plural = 'mensagens'

    def __str__(self) -> str:
        return self.message[:50]
