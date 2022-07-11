from dataclasses import fields
from email.policy import default
from rest_framework import serializers
from .models import *


class AddTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class UpdateTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TagModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class DeleteTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TagModel
        fields = ['user_id','id']

class GetTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = TagModel
        fields = ['user_id','task_id','id']









    

