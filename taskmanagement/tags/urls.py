from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('addtag/', views.addtag, name="addtag"),
	path('updatetag/', views.updatetag, name="updatetag"),
	path('deletetag/', views.deletetag, name="deletetag"),
	path('gettags/', views.gettags, name="gettags"),
	
]