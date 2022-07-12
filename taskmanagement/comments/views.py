from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from projects.models import ProjectModel
from tasks.models import TaskModel
from user_auth.models import *
from drf_yasg.utils import swagger_auto_schema
from user_auth.authentication import Authentication
# Create your views here.

@swagger_auto_schema(method='POST', request_body=AddCommentSerializer)
@api_view(["POST"])
def addnewcomment(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddCommentSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            comment_user_id = serializer.data["comment_user_id"]
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            description = serializer.data["description"]
            user = UserModel.objects.filter(id=user_id).first()
            comment_user = UserModel.objects.filter(id=comment_user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if not comment_user:
                return Response({"successs" : False,"message":"Comment user id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if user_id == comment_user_id:
                return Response({"successs" : False,"message":"User id and comment user id cannot be same"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if project_id != "":
                 project = ProjectModel.objects.filter(id=project_id).first()
                 if not project:
                    return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(task_id != ""):
                assignee = TaskModel.objects.filter(id=task_id).first()
                if not assignee:
                   return Response({"successs" : False,"message":"Task does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)  
            if(project_id == "" and task_id == ""):
                  return Response({"successs" : False,"message":"Project id and task id cannot be empty together"}, status=status.HTTP_406_NOT_ACCEPTABLE)  
            new_comment = CommentModel.objects.create(user_id=user_id,comment_user_id=comment_user_id,project_id=project_id,task_id=task_id,description=description)
            new_comment.save()
            commentdata = list(CommentModel.objects.values().filter(id=new_comment.id))
            commentdata[0].pop("is_active")
            commentdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : commentdata[0],"message":"Comment added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateCommentSerializer)
@api_view(["POST"])
def updatecomment(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateCommentSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            comment_id = serializer.data["id"]
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            description = serializer.data["description"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            comment = CommentModel.objects.filter(id=comment_id).first()
            if not comment:
                return Response({"successs" : False,"message":"Comment does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id != ""):
               projectdata = ProjectModel.objects.filter(id=project_id).first()
               if not projectdata:
                return Response({"successs" : False,"message":"Project id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(task_id != ""):
               taskdata = TaskModel.objects.filter(id=task_id).first()
               if not taskdata:
                return Response({"successs" : False,"message":"Task id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            commentdata = CommentModel.objects.filter(id=comment_id).first()
            if not commentdata:
                return Response({"successs" : False,"message":"Comment id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                   commentdata.description = description
                   commentdata.save()
                   comments = list(CommentModel.objects.values().filter(id=commentdata.id))
                   comments[0].pop("is_active")
                   comments[0].pop("is_delete")
                   return Response({"successs" : True,"data" : comments[0],"message":"Comment updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteCommentSerializer)
@api_view(["POST"])
def deletecomment(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteCommentSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            comment_id = serializer.data["id"]
            comment_user_id = serializer.data["comment_user_id"]
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            comment = CommentModel.objects.filter(id=comment_id,project_id=project_id,task_id=task_id,comment_user_id=comment_user_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            if not comment:
                return Response({"successs" : False,"message":"Comment does not exists"}, status=status.HTTP_201_CREATED)
            CommentModel.objects.filter(id=comment_id,project_id=project_id,task_id=task_id,comment_user_id=comment_user_id).delete()
            return Response({"success" : True,"message":"Comment deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetCommentSerializer)
@api_view(["POST"])
def getcomments(request):
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetCommentSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            comment_user_id = serializer.data["comment_user_id"]
            comment_id = serializer.data["id"]
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id == "" and task_id == ""):
                  return Response({"successs" : False,"message":"Project id and task id cannot be empty together"}, status=status.HTTP_406_NOT_ACCEPTABLE)  
            if (comment_id == None):
                commentdata=list(CommentModel.objects.values().filter(project_id=project_id,task_id=task_id,comment_user_id=comment_user_id))
                if not commentdata:
                 return Response({"successs" : False,"message":"No comments found"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                if(len(commentdata)==1):
                    commentdata[0].pop("is_active")
                    commentdata[0].pop("is_delete")
                    return Response({"successs" : True,"data" : commentdata[0],"message":"Comment details fetched successfully"}, status=status.HTTP_201_CREATED)
                for i in range(0,len(commentdata)):
                    commentdata[i].pop("is_active")
                    commentdata[i].pop("is_delete")
                return Response({"successs" : True,"data" : commentdata,"message":"Comment details fetched successfully"}, status=status.HTTP_201_CREATED)
            commentdata = CommentModel.objects.filter(id=comment_id,project_id=project_id,task_id=task_id,comment_user_id=comment_user_id).first()
            if not commentdata:
                return Response({"successs" : False,"message":"Comment does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                commentdata=list(CommentModel.objects.values().filter(id=comment_id,project_id=project_id,task_id=task_id,comment_user_id=comment_user_id))
                commentdata[0].pop("is_active")
                commentdata[0].pop("is_delete")
                return Response({"successs" : True,"data" : commentdata[0],"message":"Comment details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)