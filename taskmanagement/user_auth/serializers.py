from rest_framework import serializers
from .models import *
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["profile_pic","user_id","password"]
    def validate_password(self, value):
     password_validation.validate_password(value, self.instance)
     return value

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password']