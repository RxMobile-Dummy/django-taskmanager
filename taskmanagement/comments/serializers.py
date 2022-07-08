from dataclasses import fields
from rest_framework import serializers
from .models import *


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        exclude = []

class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        exclude = []

class DeleteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['user_id','project_id','task_id','comment_user_id']


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['user_id','project_id','task_id','comment_user_id']








    

