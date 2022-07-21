"""Serializers for comment module"""
from rest_framework import serializers

from comments.models import CommentModel


class AddCommentSerializer(serializers.ModelSerializer):
    """Serializers for adding comments"""
    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommentModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user_id"]


class UpdateCommentSerializer(serializers.ModelSerializer):
    """Serializers for updating comments"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommentModel
        exclude = ["created_at", "updated_at",
                   "is_active", "is_delete", "user_id"]


class DeleteCommentSerializer(serializers.ModelSerializer):
    """Serializers for deleting comments"""
    id = serializers.IntegerField()

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommentModel
        fields = ['task_id', 'comment_user_id', 'id']


class GetCommentSerializer(serializers.ModelSerializer):
    """Serializers for getting comments"""
    id = serializers.IntegerField(default=None)

    class Meta:
        """Meta class to change behaviour of model fields"""
        model = CommentModel
        fields = ['task_id', 'comment_user_id', 'id']
