from django.contrib import admin
from checklist.models import ChecklistModel

# Register your models here.
@admin.register(ChecklistModel)
class ChecklistAdmin(admin.ModelAdmin):
    pass

