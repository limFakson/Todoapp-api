
from celery import shared_task
from time import sleep
from .models import Todo, Goal

@shared_task
def add(x, y):
    return x + y

@shared_task
def sleepy(duration):
    sleep(duration)
    return 'Done'

@shared_task
def autostatus(self):
    task = Todo.objects.get()