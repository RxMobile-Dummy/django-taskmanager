"""Project Models"""
from datetime import datetime
from django.db import models


# Create your models here.
class ProjectModel(models.Model):
    """Class for project model"""
    user_id = models.CharField(max_length=50)
    color = models.CharField(max_length=50, default="", blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, default="", blank=True)
    status_id = models.CharField(max_length=50, blank=True, default="")
    duration = models.DurationField()
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    archive = models.BooleanField(default=False, blank=True)
    objects = models.Manager()


class ProjectStatusModel(models.Model):
    """Class for project status model"""
    project_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()


class ProjectAssigneeModel(models.Model):
    """Class for project assignee model"""
    project_id = models.CharField(max_length=50)
    assignee_ids = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
