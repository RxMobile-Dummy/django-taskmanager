from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('addnewtask/', views.addnewtask, name="addnewtask"),
	path('updatetask/', views.updatetask, name="updatetask"),
	path('deletetask/', views.deletetask, name="deletetask"),
	path('gettask/', views.gettask, name="gettask"),
	path('addtaskstatus/', views.addtaskstatus, name="addtaskstatus"),
	path('gettaskstatus/', views.gettaskstatus, name="gettaskstatus"),
	path('updatetaskstatus/', views.updatetaskstatus, name="updatetaskstatus"),
	path('deletetaskstatus/', views.deletetaskstatus, name="deletetaskstatus"),
]