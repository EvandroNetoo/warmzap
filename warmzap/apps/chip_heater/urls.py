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

htmx_urls = [
    path('generate-qrcode/', views.generate_qrcode, name='generate_qrcode'),
]

urlpatterns += htmx_urls
