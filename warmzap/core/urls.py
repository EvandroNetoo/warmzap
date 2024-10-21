from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(
            url=staticfiles_storage.url('general/img/favicon.ico')
        ),
    ),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('chip_heater.urls')),
    path('settings/', include('settings.urls')),
    path('payments/', include('payments.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    urlpatterns += [
        *debug_toolbar_urls(),
    ]
