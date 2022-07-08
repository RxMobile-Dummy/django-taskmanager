from dataclasses import fields
from rest_framework import serializers
from .models import *


class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = []


class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = []


class DeleteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['user_id']


class GetTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['user_id','project_id']


class AddTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusModel
        exclude = []


class GetTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusModel
        exclude = ["task_status"]


class UpdateTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusModel
        exclude = []


class DeleteTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatusModel
        exclude = ["task_status"]


    

