from django.urls import path

from accounts import views

urlpatterns = [
    path(
        'signin/',
        views.SignInView.as_view(),
        name='signin',
    ),
    path(
        'signup/',
        views.SignUpView.as_view(),
        name='signup',
    ),
    path(
        'signout/',
        views.SignOutView.as_view(),
        name='signout',
    ),
]
