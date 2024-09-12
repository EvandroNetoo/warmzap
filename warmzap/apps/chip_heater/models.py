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
        blank=True,
    )

    class Meta:
        verbose_name = 'chip'
        verbose_name_plural = 'chips'

