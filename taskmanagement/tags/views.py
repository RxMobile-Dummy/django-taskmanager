from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from tasks.models import TaskModel
from user_auth.models import *
# Create your views here.


@api_view(["POST"])
def addtag(request):
    try:
        data = request.data
        serializer = AddTagSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            task_id = serializer.data["task_id"]
            name = serializer.data["name"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            task = TaskModel.objects.filter(id=task_id).first()
            if not task:
                return Response({"successs" : False,"message":"Task does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_tag = TagModel.objects.create(user_id=user_id,task_id=task_id,name=name)
            new_tag.save()
            tagdata = list(TagModel.objects.values().filter(id=new_tag.id))
            tagdata[0].pop("is_active")
            tagdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : tagdata[0],"message":"Tag added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def updatetag(request):
    try:
        data = request.data
        serializer = UpdateTagSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            task_id = serializer.data["task_id"]
            name = serializer.data["name"]
            tag_id = serializer.data["id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            tag = TagModel.objects.filter(id=tag_id).first()
            if not tag and tag_id != "":
                return Response({"successs" : False,"message":"Tag does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(task_id != ""):
               taskdata = TaskModel.objects.filter(id=task_id).first()
               if not taskdata:
                return Response({"successs" : False,"message":"Task id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(tag_id != ""):
               tagdata = TagModel.objects.filter(id=tag_id).first()
               if not tagdata:
                return Response({"successs" : False,"message":"Tag id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               elif(tagdata.name == name):
                   return Response({"successs" : False,"message":"Tag name is same as before"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               else:
                   tagdata.name = name
                   tagdata.save()
                   tag = list(TagModel.objects.values().filter(id=tagdata.id))
                   tag[0].pop("is_active")
                   tag[0].pop("is_delete")
                   return Response({"successs" : True,"data" : tag[0],"message":"Tag name updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"successs" : False,"message":"Tag id param cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def deletetag(request):
    try:
        data = request.data
        serializer = DeleteTagSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            tag_id = serializer.data["id"]
            tag = TagModel.objects.filter(id=tag_id,user_id=user_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            if not tag:
                return Response({"successs" : False,"message":"Tag does not exists"}, status=status.HTTP_201_CREATED)
            TagModel.objects.filter(id=tag_id,user_id=user_id).delete()
            return Response({"success" : True,"message":"Tag deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def gettags(request):
    try:
        data = request.data
        serializer = GetTagSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            tag_id = serializer.data["id"] if serializer.data["id"] !="" else 0
            task_id = serializer.data["task_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(tag_id != ""):
               tagdata = TagModel.objects.filter(id=tag_id,task_id=task_id,user_id=user_id).first()
               if not tagdata:
                return Response({"successs" : False,"message":"Tag does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               else:
                tags=list(TagModel.objects.values().filter(id=tag_id,task_id=task_id,user_id=user_id))
                tags[0].pop("is_active")
                tags[0].pop("is_delete")
                return Response({"successs" : True,"data" : tags[0],"message":"Tag details fetched successfully"}, status=status.HTTP_201_CREATED)
            else:
                tagdata=list(TagModel.objects.values().filter(id=tag_id,task_id=task_id,user_id=user_id))
                if(len(tagdata)==0):
                    return Response({"successs" : True,"data" : tagdata,"message":"No tag details found"}, status=status.HTTP_201_CREATED)
                for i in range(0,len(tagdata)):
                    tagdata[i].pop("is_active")
                    tagdata[i].pop("is_delete")
                return Response({"successs" : True,"data" : tagdata,"message":"Tag details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)