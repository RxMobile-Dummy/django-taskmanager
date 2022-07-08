from dataclasses import fields
from rest_framework import serializers
from .models import *


class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        exclude = []

class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        exclude = []


class GetProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ['user_id']


class DeleteProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ['user_id']


class AddProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatusModel
        exclude = []


class GetProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatusModel
        exclude = ["project_status"]


class UpdateProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatusModel
        exclude = []


class DeleteProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatusModel
        exclude = ["project_status"]

class AddProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["assignee_ids"]

class DeleteProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["assignee_ids"]


class GetProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["assignee_ids"]


class InviteProjectAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssigneeModel
        exclude = ["assignee_ids"]
