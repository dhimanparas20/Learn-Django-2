from django.urls import path,re_path
from .consumers import *

websocket_urlpatterns = [
    # path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()), 
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
] 