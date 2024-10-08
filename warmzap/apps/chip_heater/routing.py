from django.urls import re_path

from chip_heater import consumers

websocket_urlpatterns = [
    re_path(r'ws/qrcode/', consumers.QRCodeConsumer.as_asgi()),
]
