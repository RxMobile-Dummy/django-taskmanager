from dataclasses import fields
from rest_framework import serializers
from .models import *


class AddTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        exclude = []


class UpdateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        exclude = []


class DeleteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['user_id']

class GetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['user_id','task_id']









    

