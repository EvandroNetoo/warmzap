from django.contrib import messages
from django.http import Http404, HttpRequest
from django.shortcuts import render
from django.urls import reverse

# cus_000006289658
# sub_ibnj66tis5ibjnlt
from django.utils import timezone
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from payments.asaas import Asaas
from payments.subscription_plans import (
    SUBSCRIPTION_PLANS_SETTINGS,
    SubscriptionPlanChoices,
)


class SubscriptionPlansView(View):
    template_name = 'subscription_plans.html'

    async def get(self, request: HttpRequest):
        subscription_plans = SUBSCRIPTION_PLANS_SETTINGS.copy()
        del subscription_plans[SubscriptionPlanChoices.NO_PLAN]

        context = {
            'subscription_plans': subscription_plans,
        }
        return render(request, self.template_name, context)


class SubscribePlanView(View):
    async def post(self, request: HttpRequest):
        subscription_plan_value = request.POST.get('subscription_plan')

        try:
            subscription_plan = SUBSCRIPTION_PLANS_SETTINGS[subscription_plan_value]
        except KeyError:
            raise Http404('Plano não encontrado') from None

        if not all(
            [
                request.user.name,
                request.user.surname,
                request.user.cpf,
                request.user.cellphone,
            ]
        ):
            messages.warning(
                request, 'Complete o seu cadastro para assinar o plano'
            )
            return HttpResponseClientRedirect(reverse('profile_settings'))

        if subscription_plan_value == request.user.subscription_plan:
            messages.warning(request, 'Você já está assinando este plano')
            return HttpResponseClientRedirect(reverse('subscription_plans'))

        if not request.user.asaas_customer_id:
            request.user.asaas_customer_id = await Asaas.customers.create(
                request.user
            )
            await request.user.asave()

        if not request.user.asaas_subscription_id:
            request.user.asaas_subscription_id = (
                await Asaas.subscriptions.create(
                    request.user.asaas_customer_id,
                    subscription_plan,
                )
            )
            await request.user.asave()

        else:
            await Asaas.subscriptions.update(
                request.user.asaas_subscription_id,
                {
                    'value': subscription_plan.price,
                    'nextDueDate': timezone.now().strftime('%Y-%m-%d'),
                    'description': f'Assinatura do plano {subscription_plan.label} na WarmZap',
                    'externalReference': subscription_plan.value,
                },
            )

        return HttpResponseClientRedirect(reverse('dashboard'))
