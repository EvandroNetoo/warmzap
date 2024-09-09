from accounts.models import User
from django.core.validators import RegexValidator
from django.db import models


class Chip(models.Model):
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
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{4}-\d{4}$|^\(\d{2}\) \d{5}-\d{4}$',
                message='Número de telefone inválido. O formato deve ser (xx) xxxx-xxxx ou (xx) xxxxx-xxxx.',
            )
        ],
    )

    class Meta:
        verbose_name = 'chip'
        verbose_name_plural = 'chips'
