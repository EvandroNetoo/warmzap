from chip_heater.models import Chip
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    validate_email,
)
from django.db import models

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    email = models.EmailField(
        'e-mail',
        unique=True,
        validators=[validate_email],
    )

    name = models.CharField('nome', max_length=50, blank=True)
    surname = models.CharField('sobrenome', max_length=100, blank=True)
    instagram = models.CharField(
        'instagram',
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3)],
    )
    cellphone = models.CharField(
        'telefone',
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\) \d{4,5}-\d{4}$')],
    )

    is_staff = models.BooleanField('status de staff', default=False)
    is_superuser = models.BooleanField(
        'status de super usuário',
        default=False,
    )
    date_joined = models.DateField('data de cadastro', auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    chips: models.QuerySet[Chip]

    def __str__(self) -> str:
        return self.email

    @property
    def started_chips_limit(self) -> int:
        return 3  # TODO
