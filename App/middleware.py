# middleware.py

from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser



class TokenAuthMiddleware:
    """
    Token authentication middleware for WebSocket connections.
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)

class TokenAuthMiddlewareInstance:
    """
    Token authentication middleware instance.
    """

    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.inner = middleware.inner

    async def __call__(self, receive, send):
        token = self.scope.get("query_string").decode().split("token=")[1].strip()

        try:
            token_obj = await self.get_token(token)
            self.scope["user"] = token_obj.user
        except Token.DoesNotExist:
            self.scope["user"] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)

    @database_sync_to_async
    def get_token(self, key):
        return Token.objects.get(key=key)
