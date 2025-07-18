from django.shortcuts import render
from datetime import date, timedelta
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from tasks.models import Task
from timers.models import Timer

@login_required
def home(request):
    today = date.today()

    # Tasks due today
    todays_tasks = Task.objects.filter(user=request.user, deadline=today)

    # Upcoming tasks (deadline after today)
    upcoming_tasks = Task.objects.filter(user=request.user, deadline__gt=today).order_by('deadline')[:5]

    # Total tasks count
    total_tasks = Task.objects.filter(user=request.user).count()

    # Completed tasks count
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()

    # Total estimated time in minutes
    total_estimated_minutes = 0
    for task in Task.objects.filter(user=request.user):
        et = task.estimated_time
        if et:
            total_estimated_minutes += et / 60

    actual_minutes = 0
    for timer in Timer.objects.filter(user=request.user):
        actual_minutes += timer.duration / 60

    # Prepare data for graph: estimated time (minutes) per task
    task_names = []
    estimated_minutes = []
    tasks_with_estimate = Task.objects.filter(user=request.user, estimated_time__isnull=False)

    for task in tasks_with_estimate:
        task_names.append(task.title)
        et = task.estimated_time
        estimated_minutes.append(et / 60)

    actual_minutes_per_task = []
    for task in tasks_with_estimate:
        total = Timer.objects.filter(user=request.user, task=task).aggregate(Sum('duration'))['duration__sum'] or 0
        actual_minutes_per_task.append(total / 60)

    today_seconds = Timer.objects.filter(user=request.user, task__date=today).aggregate(Sum('duration'))['duration__sum'] or 0
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_seconds = Timer.objects.filter(user=request.user, task__date__range=(week_start, week_end)).aggregate(Sum('duration'))['duration__sum'] or 0

    context = {
        "todays_tasks": todays_tasks,
        "upcoming_tasks": upcoming_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_estimated_minutes": total_estimated_minutes,
        "task_names": json.dumps(task_names),
        "estimated_minutes": json.dumps(estimated_minutes),
        "actual_minutes": json.dumps(actual_minutes),
        "actual_minutes_per_task": json.dumps(actual_minutes_per_task),
        "today_total": today_seconds,
        "week_total": week_seconds,
    }
    return render(request, "dashboard/dashboard.html", context)
