from typing import Literal
from urllib.parse import urljoin

import httpx
from accounts.models import User
from django.conf import settings
from django.utils import timezone

from payments.subscription_plans import SubscriptionPlan


class BaseAssas:
    SANDBOX_URL = 'https://sandbox.asaas.com/api/v3/'
    PRODUCTION_URL = 'https://api.asaas.com/v3/'
    ACCESS_TOKEN = settings.ASAAS_ACCESS_TOKEN

    default_headers = {
        'accept': 'application/json',
        'content-Type': 'application/json',
        'access_token': ACCESS_TOKEN,
    }

    url = SANDBOX_URL if settings.DEBUG else PRODUCTION_URL

    @classmethod
    async def post(cls, endpoint: str, data: dict, **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            url = urljoin(cls.url, endpoint)
            response = await client.post(
                url,
                json=data,
                headers=cls.default_headers,
                **kwargs,
            )

            return response.json()

    @classmethod
    async def put(cls, endpoint: str, data: dict, **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            url = urljoin(cls.url, endpoint)
            response = await client.put(
                url,
                json=data,
                headers=cls.default_headers,
                **kwargs,
            )
            return response.json()

    @classmethod
    async def get(cls, endpoint: str, **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                urljoin(cls.url, endpoint),
                headers=cls.default_headers,
                **kwargs,
            )
            return response.json()


class CustomersAssas(BaseAssas):
    base_endpoint = 'customers'

    @classmethod
    async def create(cls, user: User) -> str:
        response = await cls.post(
            cls.base_endpoint,
            {
                'name': user.full_name,
                'cpfCnpj': user.cpf,
                'email': user.email,
                'surname': user.surname,
                'mobilePhone': user.cellphone,
            },
        )
        return response.get('id')


class SubscriptionsAssas(BaseAssas):
    base_endpoint = 'subscriptions'

    @classmethod
    async def create(
        cls,
        customer_id: str,
        plan: SubscriptionPlan,
        billing_type: Literal[
            'UNDEFINED', 'BOLETO', 'CREDIT_CARD', 'PIX'
        ] = 'CREDIT_CARD',
    ) -> str:
        response = await cls.post(
            cls.base_endpoint,
            {
                'customer': customer_id,
                'billingType': billing_type,
                'value': plan.price,
                'cycle': 'MONTHLY',
                'nextDueDate': timezone.now().strftime('%Y-%m-%d'),
                'description': f'Assinatura do plano {plan.label} na WarmZap',
                'externalReference': plan.value,
                # 'split': [{'walletId': '', 'percentualValue': 20}],
            },
        )

        return response.get('id')

    @classmethod
    async def update(
        cls,
        subscription_id: str,
        data: dict,
    ) -> str:
        response = await cls.put(
            f'{cls.base_endpoint}/{subscription_id}',
            data=data,
        )
        return response.get('id')


class Asaas:
    customers = CustomersAssas
    subscriptions = SubscriptionsAssas
