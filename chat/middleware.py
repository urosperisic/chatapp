"""
JWT authentication middleware for WebSocket connections.
Extracts token from Sec-WebSocket-Protocol header and authenticates user.
"""

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_string):
    """
    Validate JWT token and return user.
    Returns AnonymousUser if token is invalid.
    """
    try:
        access_token = AccessToken(token_string)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except (TokenError, User.DoesNotExist, KeyError):
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Custom middleware for JWT authentication in WebSocket connections.
    Checks for token in subprotocol headers.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Get subprotocols from headers
        headers = dict(scope.get('headers', []))
        subprotocols_header = headers.get(b'sec-websocket-protocol', b'').decode()
        
        # Parse subprotocols - format is "authorization, <token>"
        token = None
        if subprotocols_header:
            parts = [p.strip() for p in subprotocols_header.split(',')]
            if len(parts) >= 2 and parts[0] == 'authorization':
                token = parts[1]

        # Authenticate user with token
        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)