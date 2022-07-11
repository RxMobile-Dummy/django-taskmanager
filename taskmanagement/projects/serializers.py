from dataclasses import fields
from email.policy import default
from rest_framework import serializers

from .models import *


class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        exclude = ["created_at","updated_at","is_active","is_delete","status_id"]

class UpdateProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ProjectModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class GetProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = ProjectModel
        fields = ['user_id','id']


class DeleteProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ProjectModel
        fields = ['user_id','id']


class AddProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatusModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class GetProjectStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = ProjectStatusModel
        exclude = ["project_status","created_at","updated_at","is_active","is_delete"]


class UpdateProjectStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ProjectStatusModel
        exclude = ["created_at","updated_at","is_active","is_delete"]


class DeleteProjectStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = ProjectStatusModel
        exclude = ["project_status","created_at","updated_at","is_active","is_delete"]

class AddProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["user_id","created_at","updated_at","is_active","is_delete"]

class DeleteProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["user_id","created_at","updated_at","is_active","is_delete"]


class GetProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["user_id","assignee_ids","created_at","updated_at","is_active","is_delete"]


class InviteProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["created_at","updated_at","is_active","is_delete"]
