from django.urls import path

from chip_heater import views, htmx_views

urlpatterns = [
    path(
        'dashboard/',
        views.DashboardView.as_view(),
        name='dashboard',
    ),
]

htmx_urls = [
    path(
        'add_chip/',
        htmx_views.add_chip,
        name='add_chip',
    ),
]

urlpatterns += htmx_urls
