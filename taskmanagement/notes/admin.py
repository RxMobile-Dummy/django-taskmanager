from django.contrib import admin
from notes.models import NotesModel

# Register your models here.
@admin.register(NotesModel)
class NotesModel(admin.ModelAdmin):
    pass

