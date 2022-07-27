"""Apis for task module"""
from multiprocessing import AuthenticationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from response import Response as ResponseData
from projects.models import ProjectModel
# from taskmanagement.tasks import serializers
from tasks.models import TaskModel, TaskStatusModel
from tasks.serializers import AddTaskSerializer, DeleteTaskSerializer
from tasks.serializers import AddTaskStatusSerializer, DeleteTaskStatusSerializer
from tasks.serializers import GetTaskSerializer, GetTaskStatusSerializer
from tasks.serializers import UpdateTaskSerializer, UpdateTaskStatusSerializer
from user_auth.authentication import Authentication
from user_auth.models import UserModel
import datetime

# Create your views here.


@swagger_auto_schema(method='POST', request_body=AddTaskSerializer)
@api_view(["POST"])
def add_new_task(request):
    """Function to add new task"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        start_date = data["start_date"]
        start_date = str(start_date).split("/")[2] + "-" + str(start_date).split("/")[1] + "-" + str(start_date).split("/")[0]
        data["start_date"] = start_date
        end_date = data["end_date"]
        end_date = str(end_date).split("/")[2] + "-" + str(end_date).split("/")[1] + "-" + str(end_date).split("/")[0]
        data["end_date"] = end_date
        serializer = AddTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            project_id = serializer.data["project_id"]
            name = serializer.data["name"]
            comment = serializer.data["comment"]
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            priority = serializer.data["priority"]
            reviewer_id = serializer.data["reviewer_id"]
            assignee_id = serializer.data["assignee_id"]
            tag_id = serializer.data["tag_id"]
            start_date = request.data["start_date"] if request.data["start_date"] is not None else ""
            end_date = request.data["end_date"] if request.data["end_date"] is not None else ""
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            if project_id != "":
                project = ProjectModel.objects.filter(id=project_id).first()
                if not project:
                    return Response(
                        ResponseData.error("Project does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            task_data = TaskModel.objects.filter(
                project_id=project_id, name=name).first()
            if task_data:
                return Response(
                    ResponseData.error(
                        "Task with same name exists in this project"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            if assignee_id != "":
                assignee = UserModel.objects.filter(id=assignee_id).first()
                if not assignee:
                    return Response(
                        ResponseData.error("Assignee Id does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            if reviewer_id != "":
                reviewer = UserModel.objects.filter(id=reviewer_id).first()
                if not reviewer:
                    return Response(
                        ResponseData.error("Reviewer Id does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            if reviewer_id == assignee_id is not "":
                return Response(
                    ResponseData.error(
                        "Reviewer and assignee cannot be assigned to same project"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            new_task = TaskModel.objects.create(user_id=user_id, project_id=project_id,
            name=name, comment=comment, isCompleted=False,
            description=description, is_private=is_private, priority=priority,
            reviewer_id=reviewer_id, assignee_id=assignee_id,
            tag_id=tag_id, start_date=start_date, end_date=end_date,)
            new_task.save()
            task_data = list(TaskModel.objects.values().filter(id=new_task.id))
            task_data[0].pop("is_active")
            task_data[0].pop("is_delete")
            start_date = str(task_data[0]["start_date"]).split("-")[2] + "/" + str(task_data[0]["start_date"]).split("-")[1] + "/" + str(task_data[0]["start_date"]).split("-")[0]
            task_data[0]["start_date"] = start_date
            end_date = str(task_data[0]["end_date"]).split("-")[2] + "/" + str(task_data[0]["end_date"]).split("-")[1] + "/" + str(task_data[0]["end_date"]).split("-")[0]
            task_data[0]["end_date"] = end_date
            return Response(
                ResponseData.success(task_data[0], "Task added successfully"),
                status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateTaskSerializer)
@api_view(["POST"])
def update_task(request):
    """Function to update existing task"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        start_date = data["start_date"]
        start_date = str(start_date).split("/")[2] + "-" + str(start_date).split("/")[1] + "-" + str(start_date).split("/")[0]
        data["start_date"] = start_date
        end_date = data["end_date"]
        end_date = str(end_date).split("/")[2] + "-" + str(end_date).split("/")[1] + "-" + str(end_date).split("/")[0]
        data["end_date"] = end_date
        serializer = UpdateTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            task_id = serializer.data["id"]
            project_id = serializer.data["project_id"]
            name = serializer.data["name"]
            comment = serializer.data["comment"]
            isCompleted = serializer.data["isCompleted"]
            description = serializer.data["description"]
            is_private = serializer.data["is_private"]
            priority = serializer.data["priority"]
            reviewer_id = serializer.data["reviewer_id"]
            assignee_id = serializer.data["assignee_id"]
            tag_id = serializer.data["tag_id"]
            start_date = serializer.data["start_date"]
            end_date = serializer.data["end_date"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            if project_id != "":
                project_data = ProjectModel.objects.filter(
                    id=project_id).first()
                if not project_data:
                    return Response(
                        ResponseData.error(
                            "Project id does not exists or is invalid"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            task_data = TaskModel.objects.filter(id=task_id).first()
            if not task_data:
                return Response(
                    ResponseData.error(
                        "Task id does not exists or is invalid"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            if assignee_id != "":
                assignee = UserModel.objects.filter(id=assignee_id).first()
                if not assignee:
                    return Response(
                        ResponseData.error(
                            "Assignee Id does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            if reviewer_id != "":
                reviewer = UserModel.objects.filter(id=reviewer_id).first()
                if not reviewer:
                    return Response(
                        ResponseData.error("Reviewer Id does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            if reviewer_id == assignee_id != "":
                return Response(
                    ResponseData.error(
                        "Reviewer and assignee cannot be assigned to same project"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            task = TaskModel.objects.filter(id=task_id).first()
            task.name = name
            task.comment = comment
            task.isCompleted = isCompleted
            task.description = description
            task.is_private = is_private
            task.priority = priority
            task.tag_id = tag_id
            task.reviewer_id = reviewer_id
            task.assignee_id = assignee_id
            task.start_date = start_date
            task.end_date = end_date
            task.save()
            task_data = list(TaskModel.objects.values().filter(id=task.id))
            task_data[0].pop("is_active")
            task_data[0].pop("is_delete")
            start_date = str(task_data[0]["start_date"]).split("-")[2] + "/" + str(task_data[0]["start_date"]).split("-")[1] + "/" + str(task_data[0]["start_date"]).split("-")[0]
            task_data[0]["start_date"] = start_date
            end_date = str(task_data[0]["end_date"]).split("-")[2] + "/" + str(task_data[0]["end_date"]).split("-")[1] + "/" + str(task_data[0]["end_date"]).split("-")[0]
            task_data[0]["end_date"] = end_date
            return Response(
                ResponseData.success(
                    task_data[0], "Task details updated successfully"),
                status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteTaskSerializer)
@api_view(["POST"])
def delete_task(request):
    """Function to delete task"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            task_id = serializer.data["id"]
            task = TaskModel.objects.filter(id=task_id).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("Account does not exists"),
                    status=status.HTTP_201_CREATED)
            if not task:
                return Response(
                    ResponseData.error("Task does not exists"),
                    status=status.HTTP_201_CREATED)
            TaskModel.objects.filter(id=task_id).delete()
            return Response(
                ResponseData.success_without_data("Task deleted successfully"),
                status=status.HTTP_200_OK)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetTaskSerializer)
@api_view(["POST"])
def get_task(request):
    """Function to get task details"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetTaskSerializer(data=data)
        if serializer.is_valid():
            user_id = authenticated_user[0].id
            # project_id = serializer.data["project_id"]
            # task_id = serializer.data["id"]
            date = request.data["date"] if request.data["date"] is not None else ""
            if(date !=""):
                print('str(date).split("/",2)')
                print(str(date).split("/")[2])
                date = str(date).split("/")[2] + "-" + str(date).split("/")[1] + "-" + str(date).split("/")[0]
            isCompleted = serializer.data["isCompleted"]
            user = UserModel.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            elif(date != "" and isCompleted is None):
                task_data = list(
                    TaskModel.objects.values().filter(user_id=user_id,start_date = date))
                if len(task_data) == 0:
                    return Response(
                        ResponseData.success(
                            task_data, "No task found"),
                        status=status.HTTP_201_CREATED)
                if len(task_data) == 1:
                    task_data[0].pop("is_active")
                    task_data[0].pop("is_delete")
                    start_date = str(task_data[0]["start_date"]).split("-")[2] + "/" + str(task_data[0]["start_date"]).split("-")[1] + "/" + str(task_data[0]["start_date"]).split("-")[0]
                    task_data[0]["start_date"] = start_date
                    end_date = str(task_data[0]["end_date"]).split("-")[2] + "/" + str(task_data[0]["end_date"]).split("-")[1] + "/" + str(task_data[0]["end_date"]).split("-")[0]
                    task_data[0]["end_date"] = end_date
                    return Response(
                        ResponseData.success(
                            task_data[0], "Task details fetched successfully"),
                        status=status.HTTP_201_CREATED)
                for i,ele in enumerate(task_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                    start_date = str(ele["start_date"]).split("-")[2] + "/" + str(ele["start_date"]).split("-")[1] + "/" + str(ele["start_date"]).split("-")[0]
                    ele["start_date"] = start_date
                    end_date = str(ele["end_date"]).split("-")[2] + "/" + str(ele["end_date"]).split("-")[1] + "/" + str(ele["end_date"]).split("-")[0]
                    ele["end_date"] = end_date
                return Response(
                    ResponseData.success(
                        task_data, "Task details fetched successfully"),
                    status=status.HTTP_201_CREATED)
            elif(date != "" and isCompleted is not None):
                task_data = list(
                    TaskModel.objects.values().filter(user_id=user_id,start_date = date,isCompleted = isCompleted))
                if len(task_data) == 0:
                    return Response(
                        ResponseData.success(
                            task_data, "No task found"),
                        status=status.HTTP_201_CREATED)
                if len(task_data) == 1:
                    task_data[0].pop("is_active")
                    task_data[0].pop("is_delete")
                    start_date = str(task_data[0]["start_date"]).split("-")[2] + "/" + str(task_data[0]["start_date"]).split("-")[1] + "/" + str(task_data[0]["start_date"]).split("-")[0]
                    task_data[0]["start_date"] = start_date
                    end_date = str(task_data[0]["end_date"]).split("-")[2] + "/" + str(task_data[0]["end_date"]).split("-")[1] + "/" + str(task_data[0]["end_date"]).split("-")[0]
                    task_data[0]["end_date"] = end_date
                    return Response(
                        ResponseData.success(
                            task_data[0], "Task details fetched successfully"),
                        status=status.HTTP_201_CREATED)
                for i,ele in enumerate(task_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                    start_date = str(ele["start_date"]).split("-")[2] + "/" + str(ele["start_date"]).split("-")[1] + "/" + str(ele["start_date"]).split("-")[0]
                    ele["start_date"] = start_date
                    end_date = str(ele["end_date"]).split("-")[2] + "/" + str(ele["end_date"]).split("-")[1] + "/" + str(ele["end_date"]).split("-")[0]
                    ele["end_date"] = end_date
                return Response(
                    ResponseData.success(
                        task_data, "Task details fetched successfully"),
                    status=status.HTTP_201_CREATED)
            elif(date == "" and isCompleted is not None):
                task_data = list(
                    TaskModel.objects.values().filter(user_id=user_id,isCompleted = isCompleted))
                if len(task_data) == 0:
                    return Response(
                        ResponseData.success(
                            task_data, "No task found"),
                        status=status.HTTP_201_CREATED)
                if len(task_data) == 1:
                    task_data[0].pop("is_active")
                    task_data[0].pop("is_delete")
                    start_date = str(task_data[0]["start_date"]).split("-")[2] + "/" + str(task_data[0]["start_date"]).split("-")[1] + "/" + str(task_data[0]["start_date"]).split("-")[0]
                    task_data[0]["start_date"] = start_date
                    end_date = str(task_data[0]["end_date"]).split("-")[2] + "/" + str(task_data[0]["end_date"]).split("-")[1] + "/" + str(task_data[0]["end_date"]).split("-")[0]
                    task_data[0]["end_date"] = end_date
                    return Response(
                        ResponseData.success(
                            task_data[0], "Task details fetched successfully"),
                        status=status.HTTP_201_CREATED)
                for i,ele in enumerate(task_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                    start_date = str(ele["start_date"]).split("-")[2] + "/" + str(ele["start_date"]).split("-")[1] + "/" + str(ele["start_date"]).split("-")[0]
                    ele["start_date"] = start_date
                    end_date = str(ele["end_date"]).split("-")[2] + "/" + str(ele["end_date"]).split("-")[1] + "/" + str(ele["end_date"]).split("-")[0]
                    ele["end_date"] = end_date
                return Response(
                    ResponseData.success(
                        task_data, "Task details fetched successfully"),
                    status=status.HTTP_201_CREATED)
            elif(date == "" and isCompleted is None):
                task_data = list(
                    TaskModel.objects.values().filter(user_id=user_id))
                if len(task_data) == 0:
                    return Response(
                        ResponseData.success(
                            task_data, "No task found"),
                        status=status.HTTP_201_CREATED)
                if len(task_data) == 1:
                    task_data[0].pop("is_active")
                    task_data[0].pop("is_delete")
                    start_date = str(task_data[0]["start_date"]).split("-")[2] + "/" + str(task_data[0]["start_date"]).split("-")[1] + "/" + str(task_data[0]["start_date"]).split("-")[0]
                    task_data[0]["start_date"] = start_date
                    end_date = str(task_data[0]["end_date"]).split("-")[2] + "/" + str(task_data[0]["end_date"]).split("-")[1] + "/" + str(task_data[0]["end_date"]).split("-")[0]
                    task_data[0]["end_date"] = end_date
                    return Response(
                        ResponseData.success(
                            task_data[0], "Task details fetched successfully"),
                        status=status.HTTP_201_CREATED)
                for i,ele in enumerate(task_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                    start_date = str(ele["start_date"]).split("-")[2] + "/" + str(ele["start_date"]).split("-")[1] + "/" + str(ele["start_date"]).split("-")[0]
                    ele["start_date"] = start_date
                    end_date = str(ele["end_date"]).split("-")[2] + "/" + str(ele["end_date"]).split("-")[1] + "/" + str(ele["end_date"]).split("-")[0]
                    ele["end_date"] = end_date
                return Response(
                    ResponseData.success(
                        task_data, "Task details fetched successfully"),
                    status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@ swagger_auto_schema(method='POST', request_body=AddTaskStatusSerializer)
@ api_view(["POST"])
def add_task_status(request):
    """Function to add task status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = AddTaskStatusSerializer(data=data)
        if serializer.is_valid():
            
            task_status = serializer.data["task_status"]
            status_data = TaskStatusModel.objects.filter(
                task_status=task_status).first()
            if status_data:
                return Response(
                    ResponseData.error("Task status already exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            new_task_status = TaskStatusModel.objects.create(
                task_status=task_status)
            new_task_status.save()
            task_status_data = list(
                TaskStatusModel.objects.values().filter(id=new_task_status.id))
            task_status_data[0].pop("is_active")
            task_status_data[0].pop("is_delete")
            return Response(
                ResponseData.success(
                    task_status_data[0], "Task status added successfully"),
                status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=GetTaskStatusSerializer)
@api_view(["POST"])
def get_task_status(request):
    """Function to get task status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = GetTaskStatusSerializer(data=data)
        if serializer.is_valid():
            
            task_status_id = serializer.data["id"]
            if task_status_id is None:
                task_status_data = list(TaskStatusModel.objects.values())
                if len(task_status_data) == 0:
                    return Response(
                        ResponseData.success(
                            task_status_data, "No task status found"),
                        status=status.HTTP_201_CREATED)
                if len(task_status_data) == 1:
                    task_status_data[0].pop("is_active")
                    task_status_data[0].pop("is_delete")
                    return Response(
                        ResponseData.success(
                            task_status_data[0], "Task status details fetched successfully"),
                        status=status.HTTP_201_CREATED)
                for i,ele in enumerate(task_status_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        task_status_data, "Task status details fetched successfully"),
                    status=status.HTTP_201_CREATED)
            task_status_data = TaskStatusModel.objects.filter(
                id=task_status_id).first()
            if not task_status_data:
                return Response(
                    ResponseData.error(
                        "Task status id does not exists or is invalid"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                task_status_data = list(
                    TaskStatusModel.objects.values().filter(id=task_status_id))
                task_status_data[0].pop("is_active")
                task_status_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        task_status_data[0], "Task status details fetched successfully"),
                    status=status.HTTP_201_CREATED)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=UpdateTaskStatusSerializer)
@api_view(["POST"])
def update_task_status(request):
    """Function to update task status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = UpdateTaskStatusSerializer(data=data)
        if serializer.is_valid():
            
            task_status_id = serializer.data["id"]
            task_status = serializer.data["task_status"]
            if task_status_id != "":
                task_status_data = TaskStatusModel.objects.filter(
                    id=task_status_id).first()
                if not task_status_data:
                    return Response(
                        ResponseData.error(
                            "Task status id does not exists or is invalid"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                if task_status_data.task_status == task_status:
                    return Response(
                        ResponseData.error(
                            f"The task name {task_status} already exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                task_status_data.task_status = task_status
                task_status_data.save()
                task_status_data = list(
                    TaskStatusModel.objects.values().filter(id=task_status_data.id))
                task_status_data[0].pop("is_active")
                task_status_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        task_status_data[0], "Task status updated successfully"),
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    ResponseData.error("Task status id param cannot be empty"),
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='POST', request_body=DeleteTaskStatusSerializer)
@api_view(["POST"])
def delete_task_status(request):
    """Function to delete task status"""
    try:
        authenticated_user = Authentication().authenticate(request)
        data = request.data
        serializer = DeleteTaskStatusSerializer(data=data)
        if serializer.is_valid():
            task_status_id = serializer.data["id"]
            if not TaskStatusModel.objects.filter(id=task_status_id).first():
                return Response(
                    ResponseData.error("Task status id does not exists"),
                    status=status.HTTP_201_CREATED)
            TaskStatusModel.objects.filter(id=task_status_id).delete()
            return Response(
                ResponseData.success_without_data(
                    "Task status deleted successfully"),
                status=status.HTTP_200_OK)
        return Response(ResponseData.error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response(ResponseData.error(str(exception)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
