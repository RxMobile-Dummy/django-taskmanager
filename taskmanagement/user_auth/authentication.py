from rest_framework import authentication
from rest_framework import exceptions
from .models import UserModel
from jwt_utility import *


class Authentication(authentication.BaseAuthentication):
    """
    Authenticate user using JWT utility
    """
    def authenticate(self, request):
        if 'Api-Key' in request.headers:
            token = request.headers.get('Api-Key').replace("Bearer ", "")
            if not token:
                raise exceptions.AuthenticationFailed('No token provided')
            is_valid, message = JWTUtility.is_token_valid(token)
            if is_valid:
                data = JWTUtility.decode_token(token)
                print("data")
                print(data)
                try:
                    user = UserModel.objects.filter(email=data["email"],password = data["password"]).first()
                except UserModel.DoesNotExist:
                    raise exceptions.AuthenticationFailed('No such user exists')
                return user, None
            raise exceptions.AuthenticationFailed(message)
        raise exceptions.AuthenticationFailed('No token provided')
