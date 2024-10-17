import json

from accounts.models import User
from chip_heater.models import Chip
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.db.models import F
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
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
    def dispatch(self, request, *args, **kwargs):
        subscription_plan_value = request.POST.get('subscription_plan')

        self.subscription_plan = SUBSCRIPTION_PLANS_SETTINGS.get(
            subscription_plan_value
        )
        if not self.subscription_plan:
            raise Http404('Plano não encontrado')

        if not all([
            request.user.name,
            request.user.surname,
            request.user.cpf,
            request.user.cellphone,
        ]):
            messages.warning(
                request, 'Complete o seu cadastro para assinar o plano'
            )
            return HttpResponseClientRedirect(reverse('profile_settings'))

        if subscription_plan_value == request.user.subscription_plan:
            messages.warning(request, 'Você já está assinando este plano')
            return HttpResponseClientRedirect(reverse('subscription_plans'))

        return super().dispatch(request, *args, **kwargs)

    async def post(self, request: HttpRequest):
        if not request.user.asaas_customer:
            request.user.asaas_customer = await Asaas.customers.create(
                request.user
            )

        subscription_id = (
            request.user.asaas_subscription.get('id')
            if request.user.asaas_subscription
            else None
        )
        subscription_data = {
            'value': self.subscription_plan.price,
            'nextDueDate': timezone.now().strftime('%Y-%m-%d'),
            'description': f'Assinatura do plano {self.subscription_plan.label} na WarmZap',
            'externalReference': self.subscription_plan.value,
        }

        if subscription_id:
            subscription_data['updatePendingPayments'] = True
            request.user.asaas_subscription = await Asaas.subscriptions.update(
                subscription_id,
                subscription_data,
            )
        else:
            request.user.asaas_subscription = await Asaas.subscriptions.create(
                request.user.asaas_customer.get('id'),
                self.subscription_plan,
            )

        await request.user.asave()

        payments = await Asaas.subscriptions.payments(
            request.user.asaas_subscription.get('id')
        )
        last_payment = payments[0]

        if not request.user.asaas_subscription.get('creditCard'):
            return HttpResponseClientRedirect(last_payment.get('invoiceUrl'))
        else:
            payment = await Asaas.payments.pay_with_credit_card(
                last_payment.get('id'),
                request.user.asaas_subscription.get('creditCard').get(
                    'creditCardToken'
                ),
            )

            if payment.get('status') == 'CONFIRMED':
                messages.success(
                    request,
                    'Assinatura realizada com sucesso, em instantes seu plano será atualizado',
                )
            else:
                messages.error(
                    request, 'Falha na assinatura, tente novamente mais tarde'
                )

        return HttpResponseClientRedirect(reverse('dashboard'))


@method_decorator([csrf_exempt, login_not_required], name='dispatch')
class AsaasWebhookView(View):
    @classmethod
    async def post(cls, request: HttpRequest):
        data = json.loads(request.body.decode('utf-8'))
        event = data.get('event')
        payment = data.get('payment')
        customer_id = payment.get('customer')
        user = await User.objects.annotate(
            customer_id=F('asaas_customer__id')
        ).aget(
            customer_id=customer_id,
        )

        if event in {'PAYMENT_CONFIRMED', 'PAYMENT_RECEIVED'}:
            user.subscription_plan = payment.get('externalReference')

        elif event in {'PAYMENT_OVERDUE', 'PAYMENT_REFUNDED'}:
            user.subscription_plan = SubscriptionPlanChoices.NO_PLAN

        user.asaas_subscription = await Asaas.subscriptions.get(
            user.asaas_subscription.get('id')
        )
        await user.asave()

        started_chips = (
            user.chips.filter(stage=Chip.StageChoices.STARTED)
            .annotate(days_left=F('days_to_heat') - F('heated_days'))
            .order_by('-days_left')
        )

        started_chips_count = await started_chips.acount()
        if started_chips_count > user.started_chips_limit:
            chips_to_pause = started_chips[
                : (started_chips_count - user.started_chips_limit)
            ]
            async for chip in chips_to_pause:
                chip.stage = Chip.StageChoices.NOT_STARTED
            await Chip.objects.abulk_update(chips_to_pause, ['stage'])

        return HttpResponse('OK')
