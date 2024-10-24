from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_not_required
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('chip_heater.urls')),
    path('settings/', include('settings.urls')),
    path('payments/', include('payments.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        login_not_required(serve),
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += [
        *debug_toolbar_urls(),
    ]
