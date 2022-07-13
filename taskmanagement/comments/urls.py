from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('addnewcomment/', views.addnewcomment, name="addnewcomment"),
	path('updatecomment/', views.updatecomment, name="updatecomment"),
	path('deletecomment/', views.deletecomment, name="deletecomment"),
	path('getcomments/', views.getcomments, name="getcomments"),

]