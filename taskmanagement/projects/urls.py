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
	path('deleteprojectstatus/', views.deleteProjectstatus, name="deleteprojectstatus")
]