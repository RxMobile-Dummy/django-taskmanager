from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import *
from django.http import JsonResponse
import uuid
from django.core.mail import EmailMessage  
# Create your views here.
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(["POST"])
def signup(request):
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            email_id = serializer.data["email"]
            password = serializer.data["password"]
            role = serializer.data["role"] if serializer.data["role"] !="" else 0
            mobile_number = serializer.data["mobile_number"]
            user = UserModel.objects.filter(mobile_number=mobile_number,email=email_id).first()
            roledata = UserRoleModel.objects.filter(id=role).first()
            if not roledata:
                return Response({"successs" : False,"message":"Role id is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if user:
                userdata=list(UserModel.objects.values().filter(mobile_number=mobile_number,email=email_id))
                userdata[0].pop("password")
                userdata[0].pop("is_active")
                userdata[0].pop("is_delete")
                userdata[0].pop("user_id")
                return Response({"successs" : False,"data" : userdata[0],"message":"Profile already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            UserStatusData = UserStatusModel.objects.filter(user_status="Active").first()
            user_status_id = ""
            if UserStatusData:
                user_status_id = UserStatusData.id
            new_user = UserModel.objects.create(first_name=first_name,last_name=last_name,email=email_id,mobile_number=mobile_number,password=password,role=role,
            status_id=user_status_id)
            new_user.save()
            userdetails =list(UserModel.objects.values().filter(id=new_user.id))
            userdetails[0].pop("is_active")
            userdetails[0].pop("is_delete")
            userdetails[0].pop("user_id")
            userdetails[0].pop("password")
            return Response({"successs" : True,"data" : userdetails[0],"message":"User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='POST', request_body=SignInSerializer)
@api_view(["POST"])
def signin(request):
    try:
        data = request.data
        serializer = SignInSerializer(data=data)
        if serializer.is_valid():
            password = serializer.data["password"]
            email = serializer.data["email"]
            user = UserModel.objects.filter(email=email,password=password).first()
            if not user:
                return Response({"successs" : False,"message":"Account does not exists, please register first"}, status=status.HTTP_201_CREATED)
            userdata=list(UserModel.objects.values().filter(email=email))
            userdata[0].pop("password")
            userdata[0].pop("is_active")
            userdata[0].pop("is_delete")
            userdata[0].pop("user_id")
            return JsonResponse({"successs" : True,"data" : userdata[0],"message":"User logged in successfully"}, safe=False)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='POST', request_body=ForgotPasswordSerializer)
@api_view(["POST"])
def forgotpassword(request):
    try:
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            otp = uuid.uuid4()
            mail_subject = 'Activation link has been sent to your email id'  
            email = EmailMessage(  
                        mail_subject, str(otp), to=[email]  
            )  
            emailSentID = email.send()
            print(f"SendIT : {emailSentID}")
            return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(method='POST', request_body=ResetPasswordSerializer)
@api_view(["POST"])
def resetpassword(request):
    try:
        data = request.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
         userdata = UserModel.objects.filter(id=serializer.data["user_id"]).first()
         if not userdata:
            return Response({"success" : False,"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
         if(serializer.data["password"]!=""):
          password_validation.validate_password(serializer.data["password"])
          userdata.password = serializer.data["password"]
          userdata.save()
          return Response({"success" : True,"message":"Password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteProfileSerializer)
@api_view(["POST"])
def deleteprofile(request):
    try:
        data = request.data
        serializer = DeleteProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["id"]
            if not UserModel.objects.filter(id=user_id).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            UserModel.objects.filter(id=user_id).delete()
            return Response({"success" : True,"message":"Profile deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UserUpdateProfileSerializer)
@api_view(["POST"])
def updateprofile(request):
    try:
        data = request.data
        serializer = UserUpdateProfileSerializer(data=data)
        if serializer.is_valid():
            userdata = UserModel.objects.filter(user_id=serializer.data["user_id"]).first()
            if not userdata:
                return Response({"successs" : False,"message":"Profile does not exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            role = UserRoleModel.objects.filter(id=serializer.data["role"]).first()
            if not role:
                return Response({"successs" : False,"message":"Role id is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            status_id = UserStatusModel.objects.filter(id=serializer.data["status_id"]).first()
            if not status_id:
                return Response({"successs" : False,"message":"Status id is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            userdata.first_name = serializer.data["first_name"]
            userdata.last_name = serializer.data["last_name"]
            userdata.email_id = serializer.data["email"]
            userdata.password = serializer.data["password"]
            userdata.role = serializer.data["role"]
            userdata.status_id = serializer.data["status_id"]
            userdata.mobile_number = serializer.data["mobile_number"]
            userdata.save()
            userdata=list(UserModel.objects.values().filter(user_id=serializer.data["user_id"]))
            userdata[0].pop("password")
            userdata[0].pop("is_active")
            userdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : serializer.data,"message":"User profile updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=AddUserStatusSerializer)
@api_view(["POST"])
def adduserstatus(request):
    try:
        data = request.data
        serializer = AddUserStatusSerializer(data=data)
        if serializer.is_valid():
            user_status = serializer.data["user_status"]
            user_status_data = UserStatusModel.objects.filter(user_status=user_status).first()
            if user_status_data:
                statusdata =list(UserStatusModel.objects.values().filter(user_status=user_status))
                return Response({"successs" : False,"data" : statusdata[0],"message":"This user status already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_user_status = UserStatusModel.objects.create(user_status=user_status)
            new_user_status.save()
            status_date = list(UserStatusModel.objects.values().filter(id=new_user_status.id))
            return Response({"successs" : True,"data" : status_date[0],"message":"User Status created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetUserStatusSerializer)
@api_view(["POST"])
def getuserstatus(request):
    try:
        data = request.data
        serializer = GetUserStatusSerializer(data=data)
        if serializer.is_valid():
            user_status_id = serializer.data["id"]
            if (user_status_id == None):
                userstatusdata=list(UserStatusModel.objects.values())
                if(len(userstatusdata)==1):
                    userstatusdata[0].pop("is_active")
                    userstatusdata[0].pop("is_delete")
                    return Response({"successs" : True,"data" : userstatusdata[0],"message":"User status details fetched successfully"}, status=status.HTTP_201_CREATED)
                for i in range(0,len(userstatusdata)):
                    userstatusdata[i].pop("is_active")
                    userstatusdata[i].pop("is_delete")
                return Response({"successs" : True,"data" : userstatusdata,"message":"User status details fetched successfully"}, status=status.HTTP_201_CREATED)
            userstatusdata = UserStatusModel.objects.filter(id=user_status_id).first()
            if not userstatusdata:
                return Response({"successs" : False,"message":"User status id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                userstatusdata=list(UserStatusModel.objects.values().filter(id=user_status_id))
                if(len(userstatusdata)==0):
                     return Response({"successs" : True,"data" : userstatusdata,"message":"No userstatus found"}, status=status.HTTP_201_CREATED)
                userstatusdata[0].pop("is_active")
                userstatusdata[0].pop("is_delete")
                return Response({"successs" : True,"data" : userstatusdata[0],"message":"User status details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateUserStatusSerializer)
@api_view(["POST"])
def updateuserstatus(request):
    try:
        data = request.data
        serializer = UpdateUserStatusSerializer(data=data)
        if serializer.is_valid():
            user_status_id = serializer.data["id"]
            user_status = serializer.data["user_status"]
            if(user_status_id != ""):
               userstatusdata = UserStatusModel.objects.filter(id=user_status_id).first()
               if not userstatusdata:
                return Response({"successs" : False,"message":"User status id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               if(userstatusdata.user_status == user_status):
                       return Response({"successs" : False,"message":f"The user status name {user_status} already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               userstatusdata.user_status = user_status
               userstatusdata.save()
               userstatusnewdata=list(UserStatusModel.objects.values().filter(id=userstatusdata.id))
               userstatusnewdata[0].pop("is_active")
               userstatusnewdata[0].pop("is_delete")
               return Response({"successs" : True,"data" : userstatusnewdata[0],"message":"User status updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"successs" : False,"message":"Project status id param cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteUserStatusSerializer)
@api_view(["POST"])
def deleteuserstatus(request):
    try:
        data = request.data
        serializer = DeleteUserStatusSerializer(data=data)
        if serializer.is_valid():
            user_status_id = serializer.data["id"]
            if not UserStatusModel.objects.filter(id=user_status_id).first():
                return Response({"successs" : False,"message":"User status id does not exists"}, status=status.HTTP_201_CREATED)
            UserStatusModel.objects.filter(id=user_status_id).delete()
            return Response({"success" : True,"message":"User status deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=AddUserRoleSerializer)
@api_view(["POST"])
def adduserrole(request):
    try:
        data = request.data
        serializer = AddUserRoleSerializer(data=data)
        if serializer.is_valid():
            user_role = serializer.data["user_role"]
            roledata = UserRoleModel.objects.filter(user_role=user_role).first()
            if roledata:
                rolesdata=list(UserRoleModel.objects.values().filter(user_role=user_role))
                rolesdata[0].pop("is_active")
                rolesdata[0].pop("is_delete")
                return Response({"successs" : False,"data" : rolesdata[0],"message":"This userrole already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_role = UserRoleModel.objects.create(user_role=user_role)
            new_role.save()
            role_data = list(UserRoleModel.objects.values().filter(id=new_role.id))
            role_data[0].pop("is_active")
            role_data[0].pop("is_delete")
            return Response({"successs" : True,"data" : role_data[0],"message":"User Role created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetUserRoleSerializer)
@api_view(["POST"])
def getuserrole(request):
    try:
        data = request.data
        serializer = GetUserRoleSerializer(data=data)
        if serializer.is_valid():
            user_role_id = serializer.data["id"]
            if (user_role_id == None):
                userroledata=list(UserRoleModel.objects.values())
                if(len(userroledata)==0):
                     return Response({"successs" : True,"data" : userroledata,"message":"No userrole found"}, status=status.HTTP_201_CREATED)
                if(len(userroledata)==1):
                    userroledata[0].pop("is_active")
                    userroledata[0].pop("is_delete")
                    return Response({"successs" : True,"data" : userroledata[0],"message":"User role details fetched successfully"}, status=status.HTTP_201_CREATED)
                for i in range(0,len(userroledata)):
                    userroledata[i].pop("is_active")
                    userroledata[i].pop("is_delete")
                return Response({"successs" : True,"data" : userroledata,"message":"User role details fetched successfully"}, status=status.HTTP_201_CREATED)
            userroledata = UserRoleModel.objects.filter(id=user_role_id).first()
            if not userroledata:
                return Response({"successs" : False,"message":"User role id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                userroledata=list(UserRoleModel.objects.values().filter(id=user_role_id))
                userroledata[0].pop("is_active")
                userroledata[0].pop("is_delete")
                return Response({"successs" : True,"data" : userroledata[0],"message":"User role details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateUserRoleSerializer)
@api_view(["POST"])
def updateuserrole(request):
    try:
        data = request.data
        serializer = UpdateUserRoleSerializer(data=data)
        if serializer.is_valid():
            user_role_id = serializer.data["id"]
            user_role = serializer.data["user_role"]
            if(user_role_id != ""):
               userroledata = UserRoleModel.objects.filter(id=user_role_id).first()
               if not userroledata:
                return Response({"successs" : False,"message":"User role id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               if(userroledata.user_role == user_role):
                       return Response({"successs" : False,"message":f"The user role name {user_role} already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               userroledata.user_role = user_role
               userroledata.save()
               userrolenewdata=list(UserRoleModel.objects.values().filter(id=userroledata.id))
               userrolenewdata[0].pop("is_active")
               userrolenewdata[0].pop("is_delete")
               return Response({"successs" : True,"data" : userrolenewdata[0],"message":"User role updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"successs" : False,"message":"Project status id param cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteUserRoleSerializer)
@api_view(["POST"])
def deleteuserrole(request):
    try:
        data = request.data
        serializer = DeleteUserRoleSerializer(data=data)
        if serializer.is_valid():
            user_role_id = serializer.data["id"]
            if not UserRoleModel.objects.filter(id=user_role_id).first():
                return Response({"successs" : False,"message":"User role id does not exists"}, status=status.HTTP_201_CREATED)
            UserRoleModel.objects.filter(id=user_role_id).delete()
            return Response({"success" : True,"message":"User role deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=ChangePasswordSerializer)
@api_view(["POST"])
def changepassword(request):
    try:
        data = request.data
        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            userdata = UserModel.objects.filter(id=serializer.data["user_id"],password=serializer.data["old_password"]).first()
            if not userdata:
                return Response({"successs" : False,"message":"Credentials are incorrect"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if((serializer.data["new_password"]!="" and serializer.data["old_password"]!="") and (serializer.data["new_password"] == serializer.data["old_password"])):
                return Response({"successs" : False,"message":"New password is same as previous one"}, status=status.HTTP_201_CREATED)
            if(serializer.data["new_password"]!=""):
               password_validation.validate_password(serializer.data["new_password"])
               userdata.password = serializer.data["new_password"]
               userdata.save()
               userdata=list(UserModel.objects.values().filter(id=serializer.data["user_id"]))
               return Response({"successs" : True,"message":"User password updated successfully"}, status=status.HTTP_201_CREATED)
            return Response({"successs" : False,"message":"Please provide new password value"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
