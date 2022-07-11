from dataclasses import fields
from rest_framework import serializers
from .models import *


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        exclude = ["created_at","updated_at","is_active","is_delete"]

class UpdateCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = CommentModel
        exclude = ["created_at","updated_at","is_active","is_delete"]

class DeleteCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = CommentModel
        fields = ['user_id','project_id','task_id','comment_user_id','id']


class GetCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = CommentModel
        fields = ['user_id','project_id','task_id','comment_user_id','id']








    

