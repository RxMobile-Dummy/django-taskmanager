"""Url patterns for task module"""

from django.urls import path
from . import views

urlpatterns = [
    path('add_new_task/', views.add_new_task, name="add_new_task"),
    path('update_task/', views.update_task, name="update_task"),
    path('delete_task/', views.delete_task, name="delete_task"),
    path('get_task/', views.get_task, name="get_task"),
    path('add_task_status/', views.add_task_status, name="add_task_status"),
    path('get_task_status/', views.get_task_status, name="get_task_status"),
    path('update_task_status/', views.update_task_status,
         name="update_task_status"),
    path('delete_task_status/', views.delete_task_status,
         name="delete_task_status"),
]
