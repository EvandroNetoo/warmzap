from django.urls import path

from payments import views

urlpatterns = [
    path(
        'subscription-plans/',
        views.SubscriptionPlansView.as_view(),
        name='subscription_plans',
    ),
    path(
        'subscribe-plan/',
        views.SubscribePlanView.as_view(),
        name='subscribe_plan',
    ),
    path(
        'cancel-subscription/',
        views.CancelSubscriptionView.as_view(),
        name='cancel_subscription',
    ),
    path(
        'asaas-webhook/',
        views.AsaasWebhookView.as_view(),
        name='asaas_webhook',
    ),
]
