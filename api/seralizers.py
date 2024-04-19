from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=400)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    
    class Meta:
        model = User
        fields = ['username','email', 'password']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['author', 'goal', 'task', 'limit', 'status']
        