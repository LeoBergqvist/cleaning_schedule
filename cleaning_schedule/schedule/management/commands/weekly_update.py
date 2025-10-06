# tasks/management/commands/weekly_update.py

from django.core.management.base import BaseCommand
from schedule.models import Task, Tenant  # Adjust import if models are elsewhere

class Command(BaseCommand):
    help = 'Weekly task reset: mark tasks incomplete and reassign to new tenant'

    def handle(self, *args, **options):
        # Example: Get a specific tenant to assign tasks to
        # try:
        #     new_tenant = Tenant.objects.get(name='Weekly Default')  # adjust lookup
        # except Tenant.DoesNotExist:
        #     self.stdout.write(self.style.ERROR("Tenant 'Weekly Default' does not exist."))
        #     return

        tasks = Task.objects.all()

        for task in tasks:
            task.completed = False
            #task.assigned_to = new_tenant
            task.save()
            #self.stdout.write(f"Updated task: {task.title} -> {new_tenant.name}")

        self.stdout.write(self.style.SUCCESS('Weekly task update complete.'))
