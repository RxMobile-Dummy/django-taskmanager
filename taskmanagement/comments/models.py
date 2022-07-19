"""Comments Models"""
from datetime import datetime
from django.db import models


# Create your models here.
class CommentModel(models.Model):
    """Model for comments module."""
    user_id = models.CharField(max_length=50)
    comment_user_id = models.CharField(max_length=50)
    task_id = models.CharField(max_length=50)
    description = models.CharField(max_length=300, default="", blank=True)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
