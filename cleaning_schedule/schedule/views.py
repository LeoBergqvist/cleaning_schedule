from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Task, Tenant, TaskAssignment, Room
from .forms import TenantForm, TaskForm 
from django.views.decorators.http import require_POST
import logging
logger = logging.getLogger(__name__)


# Tasks

# Gets tasks and shows them on mainpage
def task_list(request):
    #tasks = Task.objects.all().order_by('room__name')
    tasks = Task.objects.all().order_by('room__name')
    return render(request, 'schedule/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()  # creates the tenant
            # room = form.cleaned_data.get("room")
            # if room:
            #     room.tenant = tenant
            #     room.save()
            return redirect("task_list")  
    else:
        form = TaskForm()
    return render(request, "schedule/add_task.html", {"form": form})

# Gets and renders the collection of tasks
def tasks_descriptions(request):
    tasks = Task.objects.all().order_by('name')
    return render(request, 'schedule/tasks_descriptions.html', {'tasks': tasks})

def edit_task(request, pk):
    task_id = pk
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        #logger.debug(f"Tenant data: test")
        if form.is_valid():
            task = form.save(commit=False)
            new_room = form.cleaned_data.get("room")
            old_room = getattr(task, "room", None)
            # Safely remove tenant from previous room if necessary

            # Only update room if user selected a new one
            if new_room:
                #old_room = getattr(tenant, "room", None)
                if old_room and old_room != new_room:
                    old_room.task = None
                    old_room.save()

                # Assign tenant to the new room
                new_room.task = task
                new_room.save()

            elif not new_room and old_room:
                # If user explicitly cleared the room (e.g., blank form field)
                # Only unassign if they chose "empty" (optional — comment this out to prevent clearing)
                pass  # <-- keep current room

            task.save()
            return redirect("tasks_descriptions")
    else:
        form = TaskForm(instance=task)

    return render(request, "schedule/edit_task.html", {"form": form, "task": task})


    # return redirect('task-descriptions')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks_descriptions')

def task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = "done"
    task.save()
    return redirect('task_list')


def rotate_tasks(request):
    # rooms = list(Room.objects.select_related('task').order_by('id'))
    # tasks = [room.task for room in rooms]
    # rotated = tasks[-1:] + tasks[:-1]  # simple right rotation

    tasks = Task.objects.all().order_by('room__name') 
    rooms = Room.objects.all().order_by('name')

    # sanity check
    if len(tasks) != len(rooms):
        raise ValueError("Number of tasks and rooms must match for rotation.")
    i = 0
    
    for task in tasks:
        next_index = (i + 1) % len(rooms)
        task.room = rooms[next_index]
        task.status = "pending"
        i+=1
        task.save()        


    return redirect('task_list')




def reassign_task(request):
    tenants = Tenant.objects.all()

    if request.method == 'POST':
        tenant_a_id = request.POST.get('tenant_a')
        tenant_b_id = request.POST.get('tenant_b')
        week_number = request.POST.get('week_number')

        if tenant_a_id == tenant_b_id:
            return HttpResponseBadRequest("Cannot swap a tenant with themselves.")

        assignment_a = TaskAssignment.objects.filter(tenant_id=tenant_a_id, week_number=week_number).first()
        assignment_b = TaskAssignment.objects.filter(tenant_id=tenant_b_id, week_number=week_number).first()

        if not assignment_a or not assignment_b:
            return HttpResponseBadRequest("One of the tenants has no assignment for this week.")

        # Swap the assignments
        assignment_a.tenant_id, assignment_b.tenant_id = assignment_b.tenant_id, assignment_a.tenant_id
        assignment_a.save()
        assignment_b.save()

        return redirect('task_schedule')  # Make sure this named URL exists

    return render(request, 'schedule/reassign_task.html', {'tenants': tenants})


# Tenants

def add_tenant(request):
    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():           
            tenant = form.save()  # creates the tenant
            room = form.cleaned_data.get("room")
            if room:
                room.tenant = tenant
                room.save()
            return redirect("task_list")  # or wherever you want
    else:
        form = TenantForm()
    return render(request, "schedule/add_tenant.html", {"form": form})


def edit_tenant(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == "POST":
        form = TenantForm(request.POST, instance=tenant)
        logger.debug(f"Tenant data: test")
        if form.is_valid():
            tenant = form.save(commit=False)
            new_room = form.cleaned_data.get("room")
            old_room = getattr(tenant, "room", None)
            # Safely remove tenant from previous room if necessary

            # Only update room if user selected a new one
            if new_room:
                #old_room = getattr(tenant, "room", None)
                if old_room and old_room != new_room:
                    old_room.tenant = None
                    old_room.save()

                # Assign tenant to the new room
                new_room.tenant = tenant
                new_room.save()

            elif not new_room and old_room:
                # If user explicitly cleared the room (e.g., blank form field)
                # Only unassign if they chose "empty" (optional — comment this out to prevent clearing)
                pass  # <-- keep current room

            tenant.save()
            return redirect("tenant_list")
    else:
        form = TenantForm(instance=tenant)

    return render(request, "schedule/edit_tenant.html", {"form": form, "tenant": tenant})



# @require_POST
# def assignment_done(request, pk):
#     assignment = get_object_or_404(Task, pk=pk)
    
#     if assignment.status != "done":
#         assignment.status = "done"  # update status
#         assignment.save()

    # elif assignment.status != "pending":
    #     assignment.status = "pending"  # update status
    #     assignment.save()
    
    
    return redirect('task_list')  # redirect to a relevant page

def tenant_list(request):
    #tenants = Tenant.objects.all()
    tenants = Tenant.objects.all().order_by('room__name')
    return render(request, 'schedule/tenant_list.html', {'tenants': tenants})




def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    tenant.delete()
    return redirect('tenant_list')

