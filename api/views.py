from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


from .seralizers import TaskSerializer
from .models import Task

# Create your views here.
# Api overview of all api in the backend
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task/(Request sent must be GET)',
        'Detail View' : '/taskdetail/<int:pk>/(Request sent must be GET)',
        'Create' : '/task/(Request sent must be POST)',
        'Delete' : '/taskdetail/<str:pk>/(Request sent must be DELETE)',
        'Update' : '/taskdetail/<int:pk>/(Request sent must be PUT)',
    }

    return Response(api_urls)


#Authetication viewset
@api_view(['GET', 'POST'])
def userRegistration(request):
    """
    Handling Auth of the Users
    
    """

    if request.method == 'GET':
        return Response()
    

#Task viewsets
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
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise NotFound('Task not found')
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        task.delete()

        return Response("Item sucessfully delete!")
    
    return Response()
