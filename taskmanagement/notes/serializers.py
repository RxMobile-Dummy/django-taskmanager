from dataclasses import fields
from rest_framework import serializers
from .models import *


class AddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        exclude = []


class UpdateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        exclude = []


class DeleteNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        fields = ['user_id','project_id','task_id']


class GetNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        fields = ['user_id','project_id','task_id']






    

