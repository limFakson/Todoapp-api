from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User
from .seralizers import TaskSerializer
from .seralizers import UserSerializer
from .models import Task, Goal


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
def userLogin(request):
    credential = request.data.get("credential")
    password = request.data.get("password")

    if not credential or not password:
        return Response(
            {"message": "Invalid request. Both credential and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    is_email = "@" in credential

    print(f"Credential: {credential}, Password: {password}, Is Email: {is_email}")

    if is_email:
        user = authenticate(request, email=credential, password=password)
    else:
        user = authenticate(request, username=credential, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"message": "Login successful", "token": token.key},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# Registration Authetication view
@csrf_protect
@api_view(["GET", "POST"])
def userAuthetication(request):
    """
    Handling Auth of the Users

    """

    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            new_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            serializer_user = UserSerializer(new_user)
            return Response(serializer_user.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    return Response()


# Task views
@api_view(["GET", "POST"])
def task(request):
    """

    Handling GET and POST here

    """
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    return Response()


# Task Detail views
@api_view(["GET", "PUT", "DELETE"])
def taskDetail(request, pk):

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise NotFound("Task not found")

    if request.method == "GET":
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        task.delete()

        return Response("Item sucessfully delete!")

    return Response()
