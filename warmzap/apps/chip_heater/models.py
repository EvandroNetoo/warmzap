import re

from accounts.models import User
from django.db import models


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
    directory_token = models.CharField('token da pasta', max_length=50)
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
