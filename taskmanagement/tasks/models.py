"""Task module"""
import datetime
from pickle import FALSE
import django
from django.db import models

# Create your models here.

testeddate = '23/04/2015'
class TaskModel(models.Model):
    """Class for Task model"""
    user_id = models.CharField(max_length=50)
    project_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=50, blank=True, default="")
    description = models.CharField(max_length=300, default="", blank=True)
    isCompleted = models.BooleanField(max_length=200, blank=True, default=False,null=True)
    priority = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.date.today(), blank=True)
    updated_at = models.DateTimeField(default=datetime.date.today(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    tag_id = models.CharField(max_length=20, blank=True, default="")
    reviewer_id = models.CharField(max_length=20, blank=True, default="")
    assignee_id = models.CharField(max_length=20, blank=True, default="")
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    objects = models.Manager()


class TaskStatusModel(models.Model):
    """Model for task status"""
    task_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.date.today(), blank=True)
    updated_at = models.DateTimeField(default=datetime.date.today(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
