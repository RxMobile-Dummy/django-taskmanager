from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('addnewproject/', views.addnewproject, name="addnewproject"),
	path('getproject/', views.getproject, name="getproject"),
	path('updateproject/', views.updateproject, name="updateproject"),
	path('getallprojects/', views.getallprojects, name="getallprojects"),
	path('deleteproject/', views.deleteproject, name="deleteproject"),
	path('addprojectstatus/', views.addprojectstatus, name="addprojectstatus"),
	path('getprojectstatus/', views.getprojectstatus, name="getprojectstatus"),
	path('updateprojectstatus/', views.updateprojectstatus, name="updateprojectstatus"),
	path('deleteprojectstatus/', views.deleteProjectstatus, name="deleteprojectstatus"),
	path("addprojectassignee/", views.addprojectassignee, name="addprojectassignee"),
	path('deleteprojectassignee/', views.deleteprojectassignee, name="deleteprojectassignee"),
	path('getprojectassignees/', views.getprojectassignees, name="getprojectassignees"),
	path('inviteprojectassignees/', views.inviteprojectassignees, name="inviteprojectassignees"),
	path('index/<int:project_id>/<int:assignee_id>/', views.index, name='myname')
]