from django.urls import path

from .views import (
    TaskListView,
    TenantListView,
    TaskDescriptionListView,
    add_task,
    add_tenant,
    delete_task,
    delete_tenant,
    edit_task,
    edit_tenant,
    reassign_task,
    rotate_tasks,
    task_done,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("tenant-list/", TenantListView.as_view(), name="tenant_list"),
    path("tasks-descriptions/", TaskDescriptionListView.as_view(), 
         name="tasks_descriptions"),
    path("add-tenant/", add_tenant, name="add_tenant"),
    path("add-task/", add_task, name="add_task"),
    path("tenant/<int:pk>/edit/", edit_tenant, name="edit_tenant"),
    path("task/<int:pk>/edit/", edit_task, name="edit_task"),
    path("tenants/delete/<int:tenant_id>/", delete_tenant, 
         name="delete_tenant"),
    path("reassign/", reassign_task, name="reassign_task"),
    path("tasks/<int:task_id>/done/", task_done, name="task_done"),
    path("tasks/delete/<int:task_id>/", delete_task, name="delete_task"),
    path("rotate-tasks/", rotate_tasks, name="rotate_tasks"),
    
    # path('assignment/<int:pk>/done/', assignment_done, name='assignment_done'),
]
