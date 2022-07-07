from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
]