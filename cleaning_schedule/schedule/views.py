import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

import logging

from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import TaskForm, TenantForm
from .models import Room, Task, TaskAssignment, Tenant

logger = logging.getLogger(__name__)


def weather_info():

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 35.6589,
        "longitude": 139.7066,
        "hourly": ["temperature_2m", "rain", "relative_humidity_2m"],
        "timezone": "Asia/Tokyo",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    temperature = hourly.Variables(0).ValuesAsNumpy()[0]
    rain = hourly.Variables(1).ValuesAsNumpy()[0]
    humidity = hourly.Variables(2).ValuesAsNumpy()[0]
    current_weather = {
        "temperature": temperature,
        "rain": rain,
        "humidity": humidity,
        "unit": "°C"
        }
    print(current_weather)

    return current_weather

# Tasks


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.order_by("room__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your extra items:
        context["hourly_weather"] = weather_info() 
        return context
    
    
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # creates the tenant
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "schedule/add_task.html", {"form": form})


# Gets and renders the collection of tasks
class TaskDescriptionListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "schedule/tasks_descriptions.html"      

    def get_queryset(self):
        return Task.objects.order_by("name")


def edit_task(request, pk):
    task_id = pk
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            new_room = form.cleaned_data.get("room")
            old_room = getattr(task, "room", None)
            # Safely remove tenant from previous room if necessary
            
            # Only update room if user selected a new one
            if new_room:
                # old_room = getattr(tenant, "room", None)
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
    return redirect("tasks_descriptions")


def task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == "pending":
        task.status = "done"
    else:
        task.status = "pending"
    task.save()
    return redirect("task_list")


def rotate_tasks(request):
    tasks = Task.objects.all().order_by("room__name")
    rooms = Room.objects.all().order_by("name")

    # sanity check
    if len(tasks) != len(rooms):
        raise ValueError("Number of tasks and rooms must match for rotation.")
    i = 0

    for task in tasks:
        next_index = (i + 1) % len(rooms)
        task.room = rooms[next_index]
        task.status = "pending"
        i += 1
        task.save()

    return redirect("task_list")


def reassign_task(request):
    tenants = Tenant.objects.all()

    if request.method == "POST":
        tenant_a_id = request.POST.get("tenant_a")
        tenant_b_id = request.POST.get("tenant_b")
        week_number = request.POST.get("week_number")

        if tenant_a_id == tenant_b_id:
            return HttpResponseBadRequest("Cannot swap a tenant with themselves.")

        assignment_a = TaskAssignment.objects.filter(
            tenant_id=tenant_a_id, week_number=week_number
        ).first()
        assignment_b = TaskAssignment.objects.filter(
            tenant_id=tenant_b_id, week_number=week_number
        ).first()

        if not assignment_a or not assignment_b:
            return HttpResponseBadRequest(
                "One of the tenants has no assignment for this week."
            )

        # Swap the assignments
        assignment_a.tenant_id, assignment_b.tenant_id = (
            assignment_b.tenant_id,
            assignment_a.tenant_id,
        )
        assignment_a.save()
        assignment_b.save()

        return redirect("task_schedule")  # Make sure this named URL exists

    return render(request, "schedule/reassign_task.html", {"tenants": tenants})


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
            return redirect("task_list")  
    else:
        form = TenantForm()
    return render(request, "schedule/add_tenant.html", {"form": form})


def edit_tenant(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == "POST":
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            tenant = form.save(commit=False)
            new_room = form.cleaned_data.get("room")
            old_room = getattr(tenant, "room", None)
            # Safely remove tenant from previous room if necessary

            # Only update room if user selected a new one
            if new_room:
                # old_room = getattr(tenant, "room", None)
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

    return render(
        request, "schedule/edit_tenant.html", {"form": form, "tenant": tenant}
    )

    # @require_POST
    # def assignment_done(request, pk):
    #     assignment = get_object_or_404(Task, pk=pk)

    #     if assignment.status != "done":
    #         assignment.status = "done"  # update status
    #         assignment.save()

    # elif assignment.status != "pending":
    #     assignment.status = "pending"  # update status
    #     assignment.save()

    return redirect("task_list")  # redirect to a relevant page


class TenantListView(ListView):
    model = Tenant
    context_object_name = "tenants"

    def get_queryset(self):
        return Tenant.objects.order_by("room__name")


def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    tenant.delete()
    return redirect("tenant_list")
