from django.contrib import admin
from projects.models import ProjectModel,ProjectStatusModel

# Register your models here.
@admin.register(ProjectModel)
class ProjectModelAdmin(admin.ModelAdmin):
    pass

# Register your models here.
@admin.register(ProjectStatusModel)
class ProjectStatusModelAdmin(admin.ModelAdmin):
    pass