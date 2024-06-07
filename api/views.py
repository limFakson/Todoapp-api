from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
import re,random

from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth.models import User
from .seralizers import UserSerializer, GoalSerializer, TodoSerializer
from .models import Goal, Todo


# Create your views here.
# Api overview of all api in the backend
@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "Register": "/auth/reg(request method sent POST)",
        "Login": "/auth/login(request method sent POST)",
        "List": "/task/(Request method sent GET)",
        "Detail View": "/taskdetail/<int:pk>/(Request method sent GET)",
        "Create": "/task/(Request method sent POST)",
        "Delete": "/taskdetail/<str:pk>/(Request method sent DELETE)",
        "Update": "/taskdetail/<int:pk>/(Request method sent PUT)",
    }

    return Response(api_urls)


# Login Authentication View
@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def userLogin(request):
    credential = request.data.get("credential")
    password = request.data.get("password")

    if not credential or not password:
        return Response(
            {"message": "Invalid request. Both credential and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    is_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    
    if re.match(is_email, credential):
        name = User.objects.filter(email=credential)
        user = authenticate(request, username=name[0], password=password)
    else:
        user = authenticate(request, username=credential, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"message": "Login successful", "token": token.key, "user_id": user.id},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# Registration Authetication view
@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def userAuthetication(request):
    """
    Handling Auth of the Users

    """

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            try:
                new_user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                serializer_user = UserSerializer(new_user)
                return Response(serializer_user.data, status=200)
            except:
                return Response({"message":"User already exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=400)


#goal view
@api_view(["GET", "POST"])
def goals(request):
    try:
        user = request.user
    except:
        return Response({"message":"Authentication credentials were not provided. Use token keyword in authorisation"}, 
                        status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == "GET":
        goals = Goal.objects.filter(author=user)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#goal details view
@api_view(["GET", "PUT", "DELETE"])
def goal(request, pk):
    try:
        goal = Goal.objects.get(pk=pk)
    except:
        return Response({"message": "Goal does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = GoalSerializer(goal)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = GoalSerializer(goal, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    elif request.method == "DELETE":
        goal.delete()

        return Response({"message":"goal sucessfully delete!"}, status=status.HTTP_200_OK)
    return Response()
    
from datetime import datetime

# Task views
@api_view(["GET", "POST"])
def task(request, goal_id):
    """

    Handling GET and POST here

    """

    try:
        goal = Goal.objects.get(pk=goal_id)
        user = request.user
    except Goal.DoesNotExist:
        return Response({"message": "Goal not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        tasks = goal.tasks.filter(author=user)
        serializer = TodoSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(goal=goal, author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Task Detail views  cv       
@api_view(["GET", "PUT", "DELETE"])
def taskDetail(request, goal_id, pk):

    try:
        task = Todo.objects.get(pk=pk)
        user_id = request.user.id
    except Todo.DoesNotExist:
        raise NotFound("Task not found")

    if request.method == "GET":
        serializer = TodoSerializer(task)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TodoSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        task.delete()
        return Response({"message":"goal sucessfully delete!"}, status=status.HTTP_200_OK)

    return Response({"message":"Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def userId(request):
    userid = request.user.id
    return Response({"userid":userid})
    
# tasks = Task.objects.all()
# now = datetime.now()
# for i in tasks:
#     if str(i.start_time) <= str(now):
#         i.status = "ongoing"
#         i.save()
#         if str(i.end_time) <= str(now):
#             i.status = "completed"
#             i.save()
#         print(True)
#     print(i.start_time)
