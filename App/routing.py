from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi()), 
    # path("ws/chat/", ChatConsumer.as_asgi()),    
       
] 