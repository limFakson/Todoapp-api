from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Task  # Adjust the import path according to your project structure
from datetime import datetime
import logging

@shared_task
def check_and_update_task_status():
    logger = logging.getLogger(__name__)
    logger.info("Task started")

    try:
        tasks = Task.objects.filter(start_time__lte=str(datetime.now()))
        for task in tasks:
            if task.start_time <= str(datetime.now()):
                task.status = 'Ongoing'
                task.save()
        logger.info("Tasks updated successfully")
    except Exception as e:
        logger.error(f"Failed to update tasks: {e}")