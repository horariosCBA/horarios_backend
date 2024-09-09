import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Configura el entorno de Django antes de importar otros módulos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horarios_cba.settings')

# Importa la configuración de Django y otros módulos después de configurar las variables de entorno
from django.core.asgi import get_asgi_application


# Crea la aplicación ASGI de Django primero
django_asgi_app = get_asgi_application()

import api.routing

# Define la aplicación ASGI final 
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                api.routing.websocket_urlpatterns # Importa las URLs del consumidor de WebSocket
            )
        )
    ),
})

