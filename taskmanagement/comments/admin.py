from django.contrib import admin
from comments.models import CommentModel

# Register your models here.
@admin.register(CommentModel)
class CommentsAdmin(admin.ModelAdmin):
    pass

