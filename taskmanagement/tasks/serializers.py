from email.policy import default
from rest_framework import serializers
from .models import *


class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = ["created_at","updated_at","is_active","is_delete","task_status","user_id"]


class UpdateTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TaskModel
        exclude = ["created_at","updated_at","is_active","is_delete","user_id"]


class DeleteTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TaskModel
        fields = ['id']


class GetTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = TaskModel
        fields = ['project_id','id']


class AddTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class GetTaskStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = TaskStatusModel
        exclude = ["task_status","created_at","updated_at","is_active","is_delete"]


class UpdateTaskStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TaskStatusModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class DeleteTaskStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = TaskStatusModel
        exclude = ["task_status","created_at","updated_at","is_active","is_delete"]


    

