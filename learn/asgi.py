import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from App.middleware import TokenAuthMiddleware
import App.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE','gs3.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(App.routing.websocket_urlpatterns)
})


# application = ProtocolTypeRouter({
#     "websocket": TokenAuthMiddleware(
#         AuthMiddlewareStack(
#             URLRouter([
#                 path("ws/chat/<str:room_name>/", ChatConsumer),
#             ])
#         )
#     ),
# })