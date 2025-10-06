from django.db import models
from django.contrib.auth.models import User

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

# class Schedule(models.Model):
#     FREQUENCY_CHOICES = [
#         ("weekly", "Weekly"),
#     ]

#     frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="weekly")
#     day_of_week = models.IntegerField(
#         choices=[(i, day) for i, day in enumerate(
#             ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#         )]
#     )
#     start_date = models.DateField()
#     end_date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.get_frequency_display()} on {self.get_day_of_week_display()}"


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



"""
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    assigned_to = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} (Completed {self.is_completed}) Name {self.assigned_to}"
    
    def save(self, *args, **kwargs):
        # anything here?
        super().save(*args, **kwargs)  # this line must exist
    
class Tenant(models.Model):
    room = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (Room {self.room})"


class TaskAssignment(models.Model):
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    due_date = models.DateField()
    week_number = models.IntegerField(editable=False)
    is_completed = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.due_date:
            self.week_number = self.due_date.isocalendar()[1]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.task.name} → {self.tenant.name} (Week {self.week_number})"

"""