from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from todo.models import Task
from todo.renderers import TaskRenderer
from todo.serializers import TaskSerializer

class TaskRegistrationView(GenericAPIView):
    """
    View for user registration
    """
    renderer_classes = [TaskRenderer]
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_STRING),
                    }),
                'msg': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    })
    def post(self, request):
        """
        Method to run on task creation post request
        """
        serializer = TaskSerializer(data = {**request.data, 'user': request.user.id })
        if serializer.is_valid():
            # check if there is an already exisiting not complete task with same title
            existing_task = Task.objects.filter(title = request.data['title'], user = request.user).exclude(status = Task.TaskStatus.COMPLETED)
            if len(existing_task) > 0:
                return Response({
                    'errors': {
                        'non_field_errors' : ['There is already a non complete task']
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            task = serializer.save()
            return Response(
                {
                    'data': {
                        'id' : task.id,
                        'title' : task.title,
                        'description' : task.description,
                        'status' : task.status,
                        'user' : task.user.id,
                    },
                    'msg' : 'Task created'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'status': openapi.Schema(type=openapi.TYPE_STRING),
                            'user': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    ),
                ),
            }
        ),
    })
    def get(self, request):
        """
        Method to run on task get request
        """
        tasks = Task.objects.filter(user = request.user)
        serializer = TaskSerializer(tasks, many = True)
        return Response(
                {
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK
            )

class TaskDetailView(GenericAPIView):
    """
    View for task details
    """
    renderer_classes = [TaskRenderer]
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_task(self, pk, user):
        obj = get_object_or_404(Task, pk=pk, user=user)
        return obj

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'user': openapi.Schema(type=openapi.TYPE_STRING)
                    },
                ),
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    })
    def get(self, request, pk):
        """
        Method to run on task detail get request
        """
        task = self.get_task(pk = pk, user = request.user)

        serializer = TaskSerializer(task, many = False)
        return Response(
                {
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK
            )

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    })
    def delete(self, request, pk):
        """
        Method to run on task deletion request
        """
         # Ideally, we should return a 403 here if task belongs to other user.
        task = self.get_task(pk = pk, user = request.user)
        task.delete()

        return Response(
                {
                    'data': 'Task deleted successfully',
                },
                status=status.HTTP_200_OK
            )

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'errors': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
    })
    def put(self, request, pk):
        """
        Method to run on task updation request
        """
         # Ideally, we should return a 403 here if task belongs to other user.
        task = self.get_task(pk = pk, user = request.user)
        serializer = TaskSerializer(instance=task, data = {**request.data, 'user': request.user.id })
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {
                        'data': 'Task updated successfully',
                    },
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
