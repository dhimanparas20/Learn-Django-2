# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer,JsonWebsocketConsumer,async_to_sync,AsyncJsonWebsocketConsumer
from .models import *
from . serializers import *
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # query_string = self.scope['query_string'].decode('utf-8')
        # query_params = query_string.split('=')  # Split query string on '='
 
        # Access the room name from the query parameters
        # query_params = self.scope['query_string'].decode()
        # print(f"Query parameters: {query_params}")
 

        # if len(query_params) == 2:
        #     param_name = query_params[0]  # Extract parameter name
        #     param_value = query_params[1]  # Extract parameter value
        #     # print(f"Parameter name: {param_name}")
        #     # print(f"Parameter value: {param_value}")
        # else:
        #     print("Invalid query string format")
        # query_params = parse_qs(self.scope["query_string"].decode())
        # if "token" in query_params:
        #     token_key = query_params["token"][0]
        #     print(token_key)
        #     try:
        #         token_obj = Token.objects.get(key=token_key)
        #         print(token_obj)
        #         self.scope["user"] = token_obj.user
        #     except :
        #         self.scope["user"] = AnonymousUser()
        # else:
        #     self.scope["user"] = AnonymousUser()
        
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        user = self.user = self.scope["user"]
        print("---------------------")
        print(user)   
        print("---------------------")
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        try:
            if text_data:
                self.receive_json(self.decode_json(text_data), **kwargs)
            else:
                raise ValueError("No text section for incoming WebSocket frame!")
        except ValueError as e:
            self.send_json({'error': str(e)})

    def receive_json(self, content, **kwargs):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': content
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        content = event['content']

        # Send message to WebSocket
        self.send_json(content)

# class ChatConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # self.user = self.scope["user"]
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         print("-----------------------------------")
#         print(self.room_name)
#         print("-----------------------------------")
        
#         self.room_group_name = 'chat_%s' % self.room_name
#         print("-----------------------------------")
#         print(self.room_group_name)
#         print("-----------------------------------")

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         # self.user = self.scope["user"]

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data=None, bytes_data=None, **kwargs):
#         try:
#             if text_data:
#                 self.receive_json(self.decode_json(text_data), **kwargs)
#             else:
#                 raise ValueError("No text section for incoming WebSocket frame!")
#         except ValueError as e:
#             self.send_json({'error': str(e)})

#     def receive_json(self, content, **kwargs):
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'content': content
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         content = event['content']

#         # Send message to WebSocket
#         self.send_json(content)



# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.auth import AuthMiddlewareStack
# import json

# class YourConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         if self.user.is_authenticated:
#             await self.accept()
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         print("===========================================")
#         print("disconnect")
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         print("--------------------------------------")
#         print(message)
#         print("--------------------------------------")
        
#         # Here you can update your database with the received message
#         # For example, using Django ORM
#         # YourModel.objects.create(user=self.user, message=message)

#         # Optionally, send a message back to the client
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))