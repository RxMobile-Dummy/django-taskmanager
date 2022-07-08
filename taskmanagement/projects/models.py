from django.db import models
from datetime import datetime

# Create your models here.
class ProjectModel(models.Model):
    user_id = models.CharField(max_length=50)
    color = models.CharField(max_length=50,default="",blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300,default="",blank=True)
    status_id = models.CharField(max_length = 50,blank=True,default="")
    duration = models.DurationField()
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    archive = models.BooleanField(default=False,blank=True)
    
    
class ProjectStatusModel(models.Model):
    project_status = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)