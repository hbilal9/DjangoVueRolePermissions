from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get the token from query string
        query_string = scope.get("query_string", b"").decode()
        query_params = dict(x.split('=') for x in query_string.split('&') if x)
        token = query_params.get('token', None)

        if token:
            try:
                # Verify the token and get the user
                access_token = AccessToken(token)
                user_id = access_token.payload.get('user_id')
                if user_id:
                    scope['user'] = await self.get_user(user_id)
                else:
                    scope['user'] = AnonymousUser()
            except Exception as e:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        if scope['user'] == AnonymousUser():
            close_message = {
                'type': 'websocket.close',
                'message': 'Unauthorized',
                'code': 4001,  # Custom close code for unauthenticated
            }
            await send(close_message)
            return

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()