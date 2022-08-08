from django.contrib import admin
from comments.models import CommentModel
from notes.models import NotesModel
from tags.models import TagModel
from tasks.models import TaskModel,TaskStatusModel
from user_auth.models import UserModel,UserRoleModel,UserStatusModel
from projects.models import ProjectModel,ProjectAssigneeModel,ProjectStatusModel

# Register your models here.
admin.site.register(CommentModel)
admin.site.register(NotesModel)
admin.site.register(TagModel)
admin.site.register(TaskModel)
admin.site.register(TaskStatusModel)
admin.site.register(UserModel)
admin.site.register(UserRoleModel)
admin.site.register(UserStatusModel)
admin.site.register(ProjectModel)
admin.site.register(ProjectAssigneeModel)
admin.site.register(ProjectStatusModel)

