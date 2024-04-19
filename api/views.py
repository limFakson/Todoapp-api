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
        'List' : '/task/(Request sent must be GET)',
        'Detail View' : '/taskdetail/<str:pk>/(Request sent must be GET)',
        'Create' : '/task/(Request sent must be POST)',
        'Update' : '/taskdetail/<str:pk>/(Request sent must be PUT)',
        'Delete' : '/taskdetail/<str:pk>/(Request sent must be DELETE)',
    }

    return Response(api_urls)


@api_view(['GET', 'POST'])
def task(request):
    """

    Handling GET and POST here

    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    return Response()

@api_view(['GET', 'PUT', 'DELETE'])
def taskDetail(request, pk):
    
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise NotFound('Task not found')
    
    if request.method == 'GET':
        task = Task.objects.get(pk)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(instance=task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        task.delete()

        return Response("Item sucessfully delete!")
    
