import traceback
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJSONWebTokenAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings


# TODO: deprecate
class TokenAuthSupportQueryString(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"
    """
    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        # print(request.query_params['auth_token'])
        if 'auth_token' in request.query_params and \
                'HTTP_AUTHORIZATION' not in request.META:
            return self.authenticate_credentials(request.query_params.get('auth_token'))
        else:
            return super(TokenAuthSupportQueryString, self).authenticate(request)



class WsTokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    see:
    https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return WsTokenAuthMiddlewareInstance(scope, self)

class OnTheFlyJWTAuthentication(BaseJSONWebTokenAuthentication):

    @classmethod
    def decode_token(self, raw_token, verify=False):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []

        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token, verify)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })

    def authenticate_token(self, raw_token):
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

class WsTokenAuthMiddlewareInstance(OnTheFlyJWTAuthentication):
    """
    Token authorization middleware for Django Channels 2
    """

    def get_query_params(self, scope):
        return parse_qs(scope['query_string'].decode())

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner
        super(WsTokenAuthMiddlewareInstance, self).__init__()

    async def __call__(self, receive, send):
        close_old_connections()
        query_params = self.get_query_params(self.scope)
        if "auth_token" in query_params:
            try:
                auth_token = query_params['auth_token'][0]
                user, access_token = self.authenticate_token(auth_token)
                self.scope['user'] = user
            except Exception as e:
                traceback.print_exc()
                self.scope['user'] = AnonymousUser()
        inner = self.inner(self.scope)
        return await inner(receive, send)

WsTokenAuthMiddlewareStack = lambda inner: WsTokenAuthMiddleware(AuthMiddlewareStack(inner))