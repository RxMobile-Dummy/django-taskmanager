from django.contrib import admin
from tags.models import TagModel

# Register your models here.
@admin.register(TagModel)
class TagAdmin(admin.ModelAdmin):
    pass
