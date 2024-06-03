from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Goal(models.Model):
    name = models.CharField(max_length=500, default='goalname')
    description = models.CharField(max_length=2000, default='goaldescription')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.TextField(default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    goal = models.ForeignKey(Goal, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.TextField(default='Pending', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
