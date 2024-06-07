from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Goal, Todo


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=400)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = [
            "id",
            "author",
            "name",
            "goal",
            "start_time",
            "end_time",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "goal"]


class GoalSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = [
            "id",
            "author",
            "name",
            "description",
            "todos",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author"]
