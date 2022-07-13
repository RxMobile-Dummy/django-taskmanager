from dataclasses import fields
from email.policy import default
from rest_framework import serializers
from .models import *


class AddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        exclude = ["created_at","updated_at","is_active","is_delete","user_id"]


class UpdateNoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = NotesModel
        exclude = ["created_at","updated_at","is_active","is_delete","user_id"]


class DeleteNoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = NotesModel
        fields = ['project_id','task_id','id']


class GetNoteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(default=None)
    class Meta:
        model = NotesModel
        fields = ['project_id','task_id','id']






    

