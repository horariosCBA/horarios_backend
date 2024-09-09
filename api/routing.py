# routing.py
from django.urls import re_path
from .consumers import ChatConsumer

# Definimos las URL del consumidor de WebSocket
websocket_urlpatterns = [
    # URL que incluye el usuario emisor y receptor en la ruta
    re_path(r'ws/chat/(?P<usuario_emisor>\d+)/(?P<usuario_receptor>\d+)/$', ChatConsumer.as_asgi()),
]