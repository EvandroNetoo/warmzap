from django.urls import path

from chip_heater import htmx_views, views

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
    path(
        'add_chip/',
        htmx_views.add_chip,
        name='add_chip',
    ),
]

urlpatterns += htmx_urls
