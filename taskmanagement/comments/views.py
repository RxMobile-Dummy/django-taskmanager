"""Comment module"""

from multiprocessing import AuthenticationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from projects.models import ProjectModel
from tasks.models import TaskModel
from user_auth.models import UserModel
from user_auth.authentication import Authentication
from response import Response as ResponseData
from comments.models import CommentModel
from comments.serializers import AddCommentSerializer
from comments.serializers import DeleteCommentSerializer
from comments.serializers import GetCommentSerializer, UpdateCommentSerializer

# Create your views here.


@swagger_auto_schema(method="POST", request_body=AddCommentSerializer)
@api_view(["POST"])
def add_new_comment(request):
    """Function to add new comment"""
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
            user = UserModel.objects.filter(id=user_id,email = authenticated_user[0].email,mobile_number = authenticated_user[0].mobile_number).first()
            comment_user = UserModel.objects.filter(id=comment_user_id,).first()
            if not user:
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            if not comment_user:
                return Response(
                    ResponseData.error("Comment user id does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            if user_id == comment_user_id:
                return Response(
                    ResponseData.error(
                        "User id and comment user id cannot be same"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            if project_id != "":
                project = ProjectModel.objects.filter(id=project_id).first()
                if not project:
                    return Response(
                        ResponseData.error("Project does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            if task_id != "":
                assignee = TaskModel.objects.filter(id=task_id).first()
                if not assignee:
                    return Response(
                        ResponseData.error("Task does not exists"),
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            if project_id == "" and task_id == "":
                return Response(
                    ResponseData.error(
                        "Project id and task id cannot be empty together"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            new_comment = CommentModel.objects.create(
                user_id=user_id,
                comment_user_id=comment_user_id,
                project_id=project_id,
                task_id=task_id,
                description=description,
            )
            new_comment.save()
            comment_data = list(
                CommentModel.objects.values().filter(id=new_comment.id))
            comment_data[0].pop("is_active")
            comment_data[0].pop("is_delete")
            return Response(
                ResponseData.success(
                    comment_data[0], "Comment added successfully"),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=UpdateCommentSerializer)
@api_view(["POST"])
def update_comment(request):
    """Function to update an existing comment"""
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
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            comment = CommentModel.objects.filter(id=comment_id).first()
            if not comment:
                return Response(
                    ResponseData.error("Comment does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            if project_id != "":
                project_data = ProjectModel.objects.filter(
                    id=project_id).first()
                if not project_data:
                    return Response(
                        ResponseData.error(
                            "Project id does not exists or is invalid"),
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            if task_id != "":
                task_data = TaskModel.objects.filter(id=task_id).first()
                if not task_data:
                    return Response(
                        ResponseData.error(
                            "Task id does not exists or is invalid"),
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            comment_data = CommentModel.objects.filter(id=comment_id).first()
            if not comment_data:
                return Response(
                    ResponseData.error(
                        "Comment id does not exists or is invalid"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            else:
                comment_data.description = description
                comment_data.save()
                comments = list(
                    CommentModel.objects.values().filter(id=comment_data.id))
                comments[0].pop("is_active")
                comments[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        comments[0], "Comment updated successfully"),
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=DeleteCommentSerializer)
@api_view(["POST"])
def delete_comment(request):
    """Function to delete comment"""
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
            comment = CommentModel.objects.filter(
                id=comment_id,
                project_id=project_id,
                task_id=task_id,
                comment_user_id=comment_user_id,
            ).first()
            if not UserModel.objects.filter(id=user_id).first():
                return Response(
                    ResponseData.error("Account does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            if not comment:
                return Response(
                    ResponseData.error("Comment does not exists"),
                    status=status.HTTP_201_CREATED,
                )
            CommentModel.objects.filter(
                id=comment_id,
                project_id=project_id,
                task_id=task_id,
                comment_user_id=comment_user_id,
            ).delete()
            return Response(
                ResponseData.success_without_data(
                    "Comment deleted successfully"),
                status=status.HTTP_200_OK,
            )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@swagger_auto_schema(method="POST", request_body=GetCommentSerializer)
@api_view(["POST"])
def getcomments(request):
    """Function to get comments"""
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
                return Response(
                    ResponseData.error("User does not exists"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            if project_id == "" and task_id == "":
                return Response(
                    ResponseData.error(
                        "Project id and task id cannot be empty together"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            if comment_id is None:
                comment_data = list(
                    CommentModel.objects.values().filter(
                        project_id=project_id,
                        task_id=task_id,
                        comment_user_id=comment_user_id,
                    )
                )
                if not comment_data:
                    return Response(
                        ResponseData.error("No comments found"),
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
                if len(comment_data) == 1:
                    comment_data[0].pop("is_active")
                    comment_data[0].pop("is_delete")
                    return Response(
                        ResponseData.success(
                            comment_data[0], "Comment details fetched successfully"),
                        status=status.HTTP_201_CREATED,
                    )
                for i,ele in enumerate(comment_data):
                    ele.pop("is_active")
                    ele.pop("is_delete")
                return Response(
                    ResponseData.success(
                        comment_data, "Comment details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
            comment_data = CommentModel.objects.filter(
                id=comment_id,
                project_id=project_id,
                task_id=task_id,
                comment_user_id=comment_user_id,
            ).first()
            if not comment_data:
                return Response(
                    ResponseData.error(
                        "Comment does not exists or is invalid"),
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            else:
                comment_data = list(
                    CommentModel.objects.values().filter(
                        id=comment_id,
                        project_id=project_id,
                        task_id=task_id,
                        comment_user_id=comment_user_id,
                    )
                )
                comment_data[0].pop("is_active")
                comment_data[0].pop("is_delete")
                return Response(
                    ResponseData.success(
                        comment_data[0], "Comment details fetched successfully"),
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            ResponseData.error(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as exception:
        return Response(
            ResponseData.error(str(exception)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
