from django.contrib import admin
from user_auth.models import UserModel,UserRoleModel,UserStatusModel

# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserRoleModel)
class UserRoleModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserStatusModel)
class UserStatusModelAdmin(admin.ModelAdmin):
    pass