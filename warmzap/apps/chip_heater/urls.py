from django.urls import path

from chip_heater import views

urlpatterns = [
    path(
        'dashboard/',
        views.DashboardView.as_view(),
        name='dashboard',
    ),
    path(
        'my-chips/',
        views.MyChipsView.as_view(),
        name='my_chips',
    ),
]
