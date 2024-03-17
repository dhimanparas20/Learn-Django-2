import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from App.middleware import TokenAuthMiddleware
import App.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE','gs3.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                App.routing.websocket_urlpatterns
                )
        )    
    )
})