from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
	path('resetpassword/', views.resetpassword, name="resetpassword"),
    	path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
	path('resetpassword/', views.resetpassword, name="resetpassword"),
	path('changepassword/', views.changepassword, name="changepassword"),
	path('signin/', views.signin, name="signin"),
	path('deleteprofile/',views.deleteprofile,name="deleteprofile"),
	path('updateprofile/',views.updateprofile,name="updateprofile"),
	path('adduserrole/',views.adduserrole,name="adduserrole"),
	path('updateuserrole/',views.updateuserrole,name="updateuserrole"),
	path('deleteuserrole/',views.deleteuserrole,name="deleteuserrole"),
	path('getuserrole/',views.getuserrole,name="getuserrole"),
	path('adduserstatus/',views.adduserstatus,name="adduserstatus"),
	path('updateuserstatus/',views.updateuserstatus,name="updateuserstatus"),
	path('deleteuserstatus/',views.deleteuserstatus,name="deleteuserstatus"),
	path('getuserstatus/',views.getuserstatus,name="getuserstatus"),
]