from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('addnewnote/', views.addnewnote, name="addnewnote"),
	path('updatenote/', views.updatenote, name="updatenote"),
	path('deletenote/', views.deletenote, name="deletenote"),
	path('getnote/', views.getnote, name="getnote"),
]