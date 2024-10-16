from django.urls import path

from settings import views

urlpatterns = [
    path(
        'profile/',
        views.ProfileSettingsView.as_view(),
        name='profile_settings',
    ),
]
