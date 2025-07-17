from django.shortcuts import render
from datetime import date
from tasks.models import Task

def home(request):
    today = date.today()

    # Tasks due today
    todays_tasks = Task.objects.filter(deadline=today)

    # Upcoming tasks (deadline after today)
    upcoming_tasks = Task.objects.filter(deadline__gt=today).order_by('deadline')[:5]

    # Total tasks count
    total_tasks = Task.objects.count()

    # Completed tasks count
    completed_tasks = Task.objects.filter(completed=True).count()

    # Total estimated time in minutes (sum of estimated_time in minutes)
    total_estimated_minutes = 0
    for task in Task.objects.all():
        et = task.estimated_time
        if et:
            # If estimated_time is a timedelta, convert to minutes
            total_estimated_minutes += (et.total_seconds() / 60) if hasattr(et, 'total_seconds') else et

    # Prepare data for graph: estimated time (minutes) per task
    task_names = []
    estimated_minutes = []
    tasks_with_estimate = Task.objects.filter(estimated_time__isnull=False)

    for task in tasks_with_estimate:
        task_names.append(task.title)
        et = task.estimated_time
        estimated_minutes.append((et.total_seconds() / 60) if hasattr(et, 'total_seconds') else et)

    context = {
        "todays_tasks": todays_tasks,
        "upcoming_tasks": upcoming_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_estimated_minutes": total_estimated_minutes,
        "task_names": task_names,
        "estimated_minutes": estimated_minutes,
    }

    return render(request, "dashboard/home.html", context)
