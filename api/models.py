from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Goal(models.Model):
    goal = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.goal


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=False)
    task = models.CharField(max_length=500)
    limit = models.TimeField()
    status = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.task
