from django.urls import path

from .views import (
    add_task,
    add_tenant,
    delete_task,
    delete_tenant,
    edit_task,
    edit_tenant,
    reassign_task,
    rotate_tasks,
    task_done,
    task_list,
    tasks_descriptions,
    tenant_list,
)

urlpatterns = [
    path("", task_list, name="task_list"),
    path("add-tenant/", add_tenant, name="add_tenant"),
    path("add-task/", add_task, name="add_task"),
    path("tenants/", tenant_list, name="tenant_list"),
    path("tenant/<int:pk>/edit/", edit_tenant, name="edit_tenant"),
    path("task/<int:pk>/edit/", edit_task, name="edit_task"),
    path("tenants/delete/<int:tenant_id>/", delete_tenant, name="delete_tenant"),
    path("tasks-descriptions/", tasks_descriptions, name="tasks_descriptions"),
    path("reassign/", reassign_task, name="reassign_task"),
    path("tasks/<int:task_id>/done/", task_done, name="task_done"),
    path("tasks/delete/<int:task_id>/", delete_task, name="delete_task"),
    path("rotate-tasks/", rotate_tasks, name="rotate_tasks"),
    # path('assignment/<int:pk>/done/', assignment_done, name='assignment_done'),
]
