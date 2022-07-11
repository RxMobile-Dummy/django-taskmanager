from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import ProjectModel
from user_auth.models import *
from taskmanagement.email_manager import EmailManager
#importing loading from django template  
from django.template import loader  
# Create your views here.  
from django.http import HttpResponse  
# Create your views here.

@api_view(["GET"])
def index(request,project_id,assignee_id):
   projectassignees = ProjectAssigneeModel.objects.create(project_id=project_id,
   assignee_ids=assignee_id)
   projectassignees.save()
   template = loader.get_template('content.html') # getting our template  
   return HttpResponse(template.render())  

@api_view(["POST"])
def addnewproject(request):
    try:
        data = request.data
        serializer = AddProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            name = serializer.data["name"]
            color = serializer.data["color"]
            project_status_id = serializer.data["status_id"] if serializer.data["status_id"]!="" else ""
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            duration = serializer.data["duration"]
            archive = serializer.data["archive"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            projectdata = ProjectModel.objects.filter(user_id=user_id,name=name).first()    
            if projectdata:
                return Response({"successs" : False,"message":"Project with same name already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if (serializer.data["status_id"] !=""):
               projectstatusdata = ProjectStatusModel.objects.filter(id=project_status_id).first()    
               if not projectstatusdata:
                return Response({"successs" : False,"message":"Project status id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_project = ProjectModel.objects.create(user_id=user_id,
            name=name,color=color,status_id=project_status_id,description=description,is_private=is_private,archive=archive,duration=duration)
            new_project.save()
            projectdata=list(ProjectModel.objects.values().filter(id=new_project.id))
            projectdata[0].pop("is_active")
            projectdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : projectdata[0],"message":"Project added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def getproject(request):
    try:
        data = request.data
        serializer = GetProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            project_id = serializer.data["id"] if serializer.data["id"] !="" else 0
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id != ""):
               projectdata = ProjectModel.objects.filter(id=project_id).first()
               if not projectdata:
                return Response({"successs" : False,"message":"Project id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            projectdata=list(ProjectModel.objects.values().filter(id=project_id))
            projectdata[0].pop("is_active")
            projectdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : projectdata[0],"message":"Project details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def updateproject(request):
    try:
        data = request.data
        serializer = UpdateProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            project_id = serializer.data["id"] if serializer.data["id"] !="" else 0
            name = serializer.data["name"]
            color = serializer.data["color"]
            project_status_id = serializer.data["status_id"] if serializer.data["status_id"]!="" else ""
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            duration = serializer.data["duration"]
            archive = serializer.data["archive"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(project_id != ""):
               projectdata = ProjectModel.objects.filter(id=project_id).first()
               if not projectdata:
                return Response({"successs" : False,"message":"Project id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if (serializer.data["status_id"]!=""):
               projectstatusdata = ProjectStatusModel.objects.filter(id=project_status_id).first()    
               if not projectstatusdata:
                return Response({"successs" : False,"message":"Project status id does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            project = ProjectModel.objects.filter(id=project_id).first()
            project.name = name
            project.color = color
            project.status_id = project_status_id
            project.description = description
            project.is_private = is_private
            project.archive = archive
            project.duration = duration
            project.save()
            projectdata=list(ProjectModel.objects.values().filter(id=project.id))
            projectdata[0].pop("is_active")
            projectdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : projectdata[0],"message":"Project details updated successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def getallprojects(request):
    try:
        data = request.data
        serializer = GetProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            projectdata = list(ProjectModel.objects.values().filter(user_id=user_id))
            if not projectdata:
                return Response({"successs" : False,"message":"No projects found"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            for i in range(0,len(projectdata)):
                    projectdata[i].pop("is_active")
                    projectdata[i].pop("is_delete")
            return Response({"successs" : True,"data" : projectdata,"message":"Project details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def deleteproject(request):
    try:
        data = request.data
        serializer = DeleteProjectSerializer(data=data)
        if serializer.is_valid():
            user_id = serializer.data["user_id"]
            project_id = serializer.data["id"]
            if not UserModel.objects.filter(id=user_id).first():
                return Response({"successs" : False,"message":"Account does not exists"}, status=status.HTTP_201_CREATED)
            if not ProjectModel.objects.filter(id=project_id).first():
                return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_201_CREATED)
            ProjectModel.objects.filter(id=project_id).delete()
            return Response({"success" : True,"message":"Project deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def addprojectstatus(request):
    try:
        data = request.data
        serializer = AddProjectStatusSerializer(data=data)
        if serializer.is_valid():
            project_status = serializer.data["project_status"]
            statusdata = ProjectStatusModel.objects.filter(project_status=project_status).first()
            if statusdata:
                return Response({"successs" : False,"message":"Project status already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_project_status = ProjectStatusModel.objects.create(project_status=project_status)
            new_project_status.save()
            projectstatusdata = list(ProjectStatusModel.objects.values().filter(id=new_project_status.id))
            projectstatusdata[0].pop("is_active")
            projectstatusdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : projectstatusdata[0],"message":"Project status added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def getprojectstatus(request):
    try:
        data = request.data
        serializer = GetProjectStatusSerializer(data=data)
        if serializer.is_valid():
            project_status_id = serializer.data["id"] if serializer.data["id"] !="" else 0
            if(project_status_id != ""):
               projectstatusdata = ProjectStatusModel.objects.filter(id=project_status_id).first()
               if not projectstatusdata:
                return Response({"successs" : False,"message":"Project status id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               else:
                projectstatusdata=list(ProjectStatusModel.objects.values().filter(id=project_status_id))
                projectstatusdata[0].pop("is_active")
                projectstatusdata[0].pop("is_delete")
                return Response({"successs" : True,"data" : projectstatusdata,"message":"Project status details fetched successfully"}, status=status.HTTP_201_CREATED)
            else:
                projectstatusdata=list(ProjectStatusModel.objects.values())
                for i in range(0,len(projectstatusdata)):
                    projectstatusdata[i].pop("is_active")
                    projectstatusdata[i].pop("is_delete")
                return Response({"successs" : True,"data" : projectstatusdata,"message":"Project status details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def updateprojectstatus(request):
    try:
        data = request.data
        serializer = UpdateProjectStatusSerializer(data=data)
        if serializer.is_valid():
            project_status_id = serializer.data["id"]
            project_status = serializer.data["project_status"]
            if(project_status_id != ""):
               projectstatusdata = ProjectStatusModel.objects.filter(id=project_status_id).first()
               if not projectstatusdata:
                return Response({"successs" : False,"message":"Project status id does not exists or is invalid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               if(projectstatusdata.project_status == project_status):
                       return Response({"successs" : False,"message":f"The project name {project_status} already exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
               projectstatusdata.project_status = project_status
               projectstatusdata.save()
               projectstatusdata=list(ProjectStatusModel.objects.values().filter(id=projectstatusdata.id))
               projectstatusdata[0].pop("is_active")
               projectstatusdata[0].pop("is_delete")
               return Response({"successs" : True,"data" : projectstatusdata[0],"message":"Project status updated successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"successs" : False,"message":"Project status id param cannot be empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def deleteProjectstatus(request):
    try:
        data = request.data
        serializer = DeleteProjectStatusSerializer(data=data)
        if serializer.is_valid():
            project_status_id = serializer.data["id"] if serializer.data["id"] !="" else 0
            if not ProjectStatusModel.objects.filter(id=project_status_id).first():
                return Response({"successs" : False,"message":"Project status id does not exists"}, status=status.HTTP_201_CREATED)
            ProjectStatusModel.objects.filter(id=project_status_id).delete()
            return Response({"success" : True,"message":"Project status deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def addprojectassignee(request):
    try:
        data = request.data
        serializer = AddProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            project_id = serializer.data["project_id"]
            assignee_ids = serializer.data["assignee_ids"]
            assignee_ids = str(assignee_ids).split(",")
            projectdata = ProjectModel.objects.filter(id=project_id).first()    
            if not projectdata:
                return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(len(assignee_ids)!=0):
                for i in range(0,len(assignee_ids)):
                    user = UserModel.objects.filter(id=int(assignee_ids[i])).first()
                    if not user:
                         return Response({"successs" : False,"message":f"Assignee with {assignee_ids[i]} does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            for i in range(0,len(assignee_ids)):
                 existingprojectassigneedata = list(ProjectAssigneeModel.objects.values().filter(project_id=project_id,assignee_ids=assignee_ids[i]))
                 if existingprojectassigneedata:
                     return Response({"successs" : False,"message":f"Assignee with {assignee_ids[i]} already exists in this project"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                 projectassignees = ProjectAssigneeModel.objects.create(project_id=project_id,
            assignee_ids=assignee_ids[i])
                 projectassignees.save()
            projectassigneesdata=list(ProjectAssigneeModel.objects.values().filter(project_id=projectassignees.project_id))
            projectassigneesdata[0].pop("is_active")
            projectassigneesdata[0].pop("is_delete")
            return Response({"successs" : True,"data" : projectassigneesdata,"message":"Project assignees added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(["POST"])
def deleteprojectassignee(request):
    try:
        data = request.data
        serializer = DeleteProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            project_id = serializer.data["project_id"]
            assignee_ids = serializer.data["assignee_ids"]
            assignee_ids = str(assignee_ids).split(",")
            projectdata = ProjectModel.objects.filter(id=project_id).first()    
            if not projectdata:
                return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(len(assignee_ids)!=0):
                for i in range(0,len(assignee_ids)):
                    user = UserModel.objects.filter(id=int(assignee_ids[i])).first()
                    if not user:
                         return Response({"successs" : False,"message":f"Assignee with {assignee_ids[i]} does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    ProjectAssigneeModel.objects.filter(assignee_ids=assignee_ids[i]).delete()
            
            return Response({"successs" : True,"message":"assignees deleted successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def getprojectassignees(request):
    try:
        data = request.data
        serializer = GetProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            project_id = serializer.data["project_id"]
            projectdata = list(ProjectModel.objects.values().filter(id=project_id))
            if not projectdata:
                return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            projectassigneedata = list(ProjectAssigneeModel.objects.values().filter(project_id=project_id))
            if (len(projectassigneedata) == 0):
                return Response({"successs" : True,"data" : [],"message":"No project assignee found"}, status=status.HTTP_201_CREATED)
            for i in range(0,len(projectassigneedata)):
                    projectassigneedata[i].pop("is_active")
                    projectassigneedata[i].pop("is_delete")
            return Response({"successs" : True,"data" : projectassigneedata,"message":"Project assignee details fetched successfully"}, status=status.HTTP_201_CREATED)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def inviteprojectassignees(request):
    try:
        data = request.data
        serializer = InviteProjectAssigneeSerializer(data=data)
        if serializer.is_valid():
            project_id = serializer.data["project_id"]
            assignee_ids = serializer.data["assignee_ids"]
            assignee_ids = str(assignee_ids).split(",")
            user_id = serializer.data["user_id"]
            projectdata = ProjectModel.objects.filter(id=project_id).first()    
            userdata = UserModel.objects.filter(id=user_id).first() 
            if not userdata:
                return Response({"successs" : False,"message":"User does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if not projectdata:
                return Response({"successs" : False,"message":"Project does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if(len(assignee_ids)!=0):
                for i in range(0,len(assignee_ids)):
                    user = UserModel.objects.filter(id=int(assignee_ids[i])).first()
                    if not user:
                         return Response({"successs" : False,"message":f"Assignee with {assignee_ids[i]} does not exists"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            for i in range(0,len(assignee_ids)):
                existingprojectassigneedata = ProjectAssigneeModel.objects.values().filter(project_id=project_id,assignee_ids=assignee_ids[i])
                if existingprojectassigneedata:
                     return Response({"successs" : False,"message":f"Assignee with {assignee_ids[i]} already exists in this project"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                assigneedata = UserModel.objects.filter(id=assignee_ids[i]).first() 
                if assigneedata:
                    return Response(EmailManager().sendEmail(assigneedata.email,"Forgot Password","",project_id,assigneedata.id), status=status.HTTP_200_OK)
        return Response({"success" : False,"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



