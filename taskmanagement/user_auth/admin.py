from django import forms
from django.contrib import admin
from django.forms import PasswordInput
from user_auth.models import UserModel,UserRoleModel,UserStatusModel

class UserForm(forms.ModelForm):
   class Meta:
     widgets = {
      'password': PasswordInput,
}

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    form = UserForm
    pass

@admin.register(UserRoleModel)
class UserRoleModelAdmin(admin.ModelAdmin):
    pass

@admin.register(UserStatusModel)
class UserStatusModelAdmin(admin.ModelAdmin):
    pass