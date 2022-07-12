import jwt

from user_auth.models import UserModel
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django_jwt_extended.apps import DjangoJwtExtConfig
from django.apps import apps


from taskmanagement import settings

class JWTUtility(object):
    """
    JWT Utility contains utility methods for dealing with JWTokens using Python JWT

    - JWT_TOKEN_EXPIRY: No. of minutes
    """
    JWT_TOKEN_EXPIRY = getattr(settings, 'JWT_TOKEN_EXPIRY', timedelta(minutes=30))

    @staticmethod
    def encode_token(UserModel):
        """
        Token created against username of the user.
        """
        if UserModel:
            data = {
                'exp': datetime.utcnow() + timedelta(days=settings.JWT_TOKEN_EXPIRY),
                'email': UserModel.email,
                'password' : UserModel.password
            }
            config = apps.get_app_config('django_jwt_extended')
            refreshdata = {
                'exp': datetime.utcnow() + config.refresh_token_expires,
                'email': UserModel.email,
                'password' : UserModel.password
            }
            token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            return {
        'refresh': str(jwt.encode(refreshdata, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)).replace("b'", "").replace("'", ""),
        'access': str(token).replace("b'", "").replace("'", ""),
    }
        # raise User.DoesNotExist

    @staticmethod
    def is_token_valid(token):
        """
        Check if token is valid.
        """
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
            return True, "Valid"
        except jwt.ExpiredSignatureError:
            return False, "Token Expired"
        except jwt.InvalidTokenError:
            return False, "Token is Invalid"

    @staticmethod
    def decode_token(token):
        """
        return user for the token given.
        """
        username_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        print("username_dict")
        print(username_dict)
        return username_dict
