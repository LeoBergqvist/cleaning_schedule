from django.contrib import admin

from .models import Room, Task, TaskAssignment, TaskLog, Tenant

admin.site.register(Tenant)
admin.site.register(Room)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskLog)
