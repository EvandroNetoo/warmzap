from django.urls import path

from phone_heater import views

urlpatterns = [
    path(
        'dashboard/',
        views.DashboardView.as_view(),
        name='dashboard',
    )
]
