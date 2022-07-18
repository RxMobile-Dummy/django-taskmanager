"""Task module"""
from datetime import datetime
from django.db import models

# Create your models here.


class TaskModel(models.Model):
    """Class for Task model"""
    user_id = models.CharField(max_length=50)
    project_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=50, blank=True, default="")
    description = models.CharField(max_length=300, default="", blank=True)
    task_status = models.CharField(max_length=200, blank=True, default="")
    priority = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    tag_id = models.CharField(max_length=20, blank=True, default="")
    reviewer_id = models.CharField(max_length=20, blank=True, default="")
    assignee_id = models.CharField(max_length=20, blank=True, default="")
    start_date = models.DateTimeField(default=datetime.now(), blank=True)
    end_date = models.DateTimeField(default=datetime.now(), blank=True)
    objects = models.Manager()


class TaskStatusModel(models.Model):
    """Model for task status"""
    task_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
