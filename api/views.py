from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


from .seralizers import TaskSerializer
from .models import Task

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Detail View' : '/task-detail/<str:pk>/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete /<str:pk>/',
    }

    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetails(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['PUT'])
def taskUpdate(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise NotFound('Task not found')

    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response("Item sucessfully delete!")