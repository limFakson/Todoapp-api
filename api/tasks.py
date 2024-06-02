from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Task  # Adjust the import path according to your project structure
from datetime import datetime

@shared_task
def check_and_update_task_status():
    tasks = Task.objects.filter(start_time__lte=datetime.now())
    for task in tasks:
        if task.start_time <= datetime.now() < task.end_time:
            task.status = 'Ongoing'
            task.save()