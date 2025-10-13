# tasks/management/commands/weekly_update.py

from django.core.management.base import BaseCommand

from schedule.models import Task, Tenant  # Adjust import if models are elsewhere


class Command(BaseCommand):
    help = 'Weekly task reset: mark tasks incomplete and reassign to new tenant'

    def handle(self, *args, **options):
        tasks = Task.objects.all()
        tenants = list(Tenant.objects.all())

        number_of_tenants = len(tenants) # out of bounds check
        for task in tasks:
            task.is_completed = False
            assigned_to = task.assigned_to
            assigned_to_index = tenants.index(assigned_to)

            new_index = (assigned_to_index + 1) % number_of_tenants
            new_assigned_to = tenants[new_index]
            task.assigned_to = new_assigned_to

            task.save()

        self.stdout.write(self.style.SUCCESS('Weekly task update complete.'))
