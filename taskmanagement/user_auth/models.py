"""Serializer for usermodel"""

from datetime import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class UserModel(models.Model):
    """Serializer for user model"""
    first_name = models.CharField(max_length=50, blank=False)
    user_id = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50)
    status_id = models.CharField(max_length=50, default="")
    profile_pic = models.FileField(blank=True)
    email = models.EmailField()
    mobile_number = PhoneNumberField()
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()


class UserRoleModel(models.Model):
    """Serializer for user role"""
    user_role = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()


class UserStatusModel(models.Model):
    """Serializer for user status"""
    user_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

class OtpForPasswordModel(models.Model):
    """Serializer for user status"""
    user_id = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    otp = models.IntegerField(max_length=6)
