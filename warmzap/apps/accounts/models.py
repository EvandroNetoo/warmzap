from chip_heater.models import Chip
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import (
    MinLengthValidator,
    RegexValidator,
    validate_email,
)
from django.db import models
from payments.subscription_plans import (
    SUBSCRIPTION_PLANS_SETTINGS,
    SubscriptionPlan,
    SubscriptionPlanChoices,
)

from accounts.managers import UserManager
from accounts.validators import validate_cpf


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
        validators=[MinLengthValidator(3)],
    )
    cellphone = models.CharField(
        'telefone',
        max_length=15,
        validators=[RegexValidator(r'^\(\d{2}\) \d{4,5}-\d{4}$')],
    )
    cpf = models.CharField(
        'CPF',
        max_length=14,
        blank=True,
        validators=[
            RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'),
            validate_cpf,
        ],
    )

    subscription_plan = models.CharField(
        'plano de assinatura',
        max_length=20,
        choices=SubscriptionPlanChoices.choices,
        default=SubscriptionPlanChoices.NO_PLAN,
    )

    asaas_customer = models.JSONField('clinte do asaas', blank=True, null=True)
    asaas_subscription = models.JSONField(
        'assinatura do asaas', blank=True, null=True
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
    def full_name(self) -> str:
        return f'{self.name} {self.surname}'

    @property
    def started_chips_limit(self) -> int:
        return self.subscription_plan_settings.chips_limit

    @property
    def subscription_plan_settings(self) -> SubscriptionPlan:
        return SUBSCRIPTION_PLANS_SETTINGS[self.subscription_plan]
