"""Tag Model class"""
from datetime import datetime
from django.db import models

# Create your models here.


class TagModel(models.Model):
    """Class for tag model"""
    user_id = models.CharField(max_length=50)
    task_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()
