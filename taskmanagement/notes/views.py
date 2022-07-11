from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from projects.models import ProjectModel
from tasks.models import TaskModel
from user_auth.models import *
# Create your views here.


@api_view(["POST"])
def addnewnote(request):
    try:
        data = request.data
        serializer = AddNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            title = serializer.data["title"]
            description = serializer.data["description"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if project_id != "":
                 project = ProjectModel.objects.filter(id=project_id).first()
                 if not project:
                    return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(task_id != ""):
                assignee = TaskModel.objects.filter(id=task_id).first()
                if not assignee:
                   return Response({"successs" : False,"message":"Task does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)    
            new_note = NotesModel.objects.create(user_id=user_id,project_id=project_id,task_id=task_id,title=title,description=description)
            new_note.save()
            notedata = list(NotesModel.objects.values().filter(id=new_note.id))
            notedata[0].pop("is_active")
            notedata[0].pop("is_delete")
            return Response({"successs" : True,"data" : notedata[0],"message":"Note added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def updatenote(request):
    try:
        data = request.data
        serializer = UpdateNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            note_id = serializer.data["id"] if serializer.data["id"] !="" else 0
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            title = serializer.data["title"]
            description = serializer.data["description"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id != ""):
               projectdata = ProjectModel.objects.filter(id=project_id).first()
               if not projectdata:
                return Response({"successs" : False,"message":"Project id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(task_id != ""):
               taskdata = TaskModel.objects.filter(id=task_id).first()
               if not taskdata:
                return Response({"successs" : False,"message":"Task id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(note_id != ""):
               notesdata = NotesModel.objects.filter(id=note_id).first()
               if not notesdata:
                return Response({"successs" : False,"message":"Note id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               else:
                   note = NotesModel.objects.filter(id=note_id).first()
                   note.title = title
                   note.description = description
                   note.save()
                   notedata=list(NotesModel.objects.values().filter(id=note.id))
                   notedata[0].pop("is_active")
                   notedata[0].pop("is_delete")
                   return Response({"successs" : True,"data" : notedata[0],"message":"Note details updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"successs" : False,"message":"Note id param cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def deletenote(request):
    try:
        data = request.data
        serializer = DeleteNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            note_id = serializer.data["id"]
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            note = NotesModel.objects.filter(id=note_id,project_id=project_id,task_id=task_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            if not note:
                return Response({"successs" : False,"message":"Note does not exists"}, status=status.HTTP_201_CREATED)
            NotesModel.objects.filter(id=note_id,project_id=project_id,task_id=task_id).delete()
            return Response({"success" : True,"message":"Note deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def getnote(request):
    try:
        data = request.data
        serializer = GetNoteSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            note_id = serializer.data["id"] if data["id"] !="" else 0
            project_id = serializer.data["project_id"]
            task_id = serializer.data["task_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(note_id != ""):
               notedata = NotesModel.objects.filter(id=note_id).first()
               if not notedata:
                return Response({"successs" : False,"message":"Note id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               else:
                notedata=list(NotesModel.objects.values().filter(id=note_id,project_id=project_id,task_id=task_id))
                notedata[0].pop("is_active")
                notedata[0].pop("is_delete")
                return Response({"successs" : True,"data" : notedata,"message":"Note details fetched successfully"}, status=status.HTTP_201_CREATED)
            else:
                notedata=list(NotesModel.objects.values().filter(project_id=project_id,task_id=task_id))
                for i in range(0,len(notedata)):
                    notedata[i].pop("is_active")
                    notedata[i].pop("is_delete")
                return Response({"successs" : True,"data" : notedata,"message":"Note details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)