import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from .models import Task

class Command(BaseCommand):
    help = "Check tasks and update status"

    def handle(self, *args, **options):
        now = timezone.now()
        tasks = Task.objects.filter(start_time=now, status="pending")
        print(tasks)
        for task in tasks:
            task.status = "ongoing"
            task.save()
            # self.stdout.write(self.style.SUCCESS(f"Task {(link unavailable)} status updated to ongoing"))