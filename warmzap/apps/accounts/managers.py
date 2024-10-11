from typing import Any

from chip_heater.models import Chip
from django.contrib.auth.models import BaseUserManager
from django.db.models import Count, Q


class UserManager(BaseUserManager):
    def _create_user(
        self,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> None:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(
        self,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super User must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related('chips')
            .annotate(
                qtd_started_chip=Count(
                    'chips', filter=Q(chips__stage=Chip.StageChoices.STARTED)
                )
            )
        )
