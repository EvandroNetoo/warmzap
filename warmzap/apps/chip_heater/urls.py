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
        'start-heating/<str:chip_pk>/',
        htmx_views.StartHeatingView.as_view(),
        name='start_heating',
    )
]

urlpatterns += htmx_urls
