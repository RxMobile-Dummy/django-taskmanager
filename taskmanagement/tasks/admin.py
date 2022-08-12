from django.contrib import admin
from tasks.models import TaskModel,TaskStatusModel

# Register your models here.
@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(TaskStatusModel)
class TaskStatusAdmin(admin.ModelAdmin):
    pass
