from rest_framework import serializers

from jwt_utility import *
from .models import *
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        exclude = ["profile_pic","user_id","created_at","updated_at","is_active","is_delete","status_id"]
    def validate_password(self, value):
     password_validation.validate_password(value, self.instance)
     return value
     
    def get_token(self, user):
        return JWTUtility.encode_token(user)


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password']

class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email']

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password']

class UserUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ["profile_pic","user_id","created_at","updated_at","is_active","is_delete"]


class DeleteProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = UserModel
        fields = ['id']


class AddUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatusModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class GetUserStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = UserStatusModel
        exclude = ["user_status","created_at","updated_at","is_active","is_delete"]


class UpdateUserStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = UserStatusModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class DeleteUserStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = UserStatusModel
        exclude = ["user_status","created_at","updated_at","is_active","is_delete"]


class AddUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class GetUserRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = UserRoleModel
        exclude = ["user_role","created_at","updated_at","is_active","is_delete"]


class UpdateUserRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = UserRoleModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class DeleteUserRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = UserRoleModel
        exclude = ["user_role","created_at","updated_at","is_active","is_delete"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    class Meta:
        model = UserModel
        fields = ['user_id','old_password','new_password']
    def validate_password(self, value):
     password_validation.validate_password(value, self.instance)
     return value
