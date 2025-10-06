from django.contrib import admin
from .models import Tenant, Room, Task, TaskAssignment, TaskLog

admin.site.register(Tenant)
admin.site.register(Room)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskLog)