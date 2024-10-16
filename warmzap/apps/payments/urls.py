from django.urls import path

from payments import views

urlpatterns = [
    path(
        'subscription_plans/',
        views.SubscriptionPlansView.as_view(),
        name='subscription_plans',
    ),
    path(
        'subscribe_plan/',
        views.SubscribePlanView.as_view(),
        name='subscribe_plan',
    ),
]
