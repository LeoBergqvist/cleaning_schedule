from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    tenant = models.OneToOneField(Tenant, on_delete=models.SET_NULL,
                                  related_name="room", null=True, blank=True)

    def __str__(self):
            return f"{self.name} ({self.tenant.name if self.tenant else 'empty'})"

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("done", "Done"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name="assigned")
    #schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="assignments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.name


class TaskAssignment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("done", "Done"),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignments")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="assignments")
    #schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="assignments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.task.name} → {self.room.name}"


class TaskLog(models.Model):
    task_assignment = models.ForeignKey(TaskAssignment, on_delete=models.CASCADE, related_name="logs")
    scheduled_date = models.DateField()
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.task_assignment.task.name} on {self.scheduled_date}"
