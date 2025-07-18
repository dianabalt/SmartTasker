from django.utils import timezone
from django.shortcuts import render
from datetime import date, timedelta
import json
from django.contrib.auth.decorators import login_required
from tasks.models import Task
from timers.models import Timer
from django.db.models import Sum


def get_total_elapsed_seconds(user, task=None):
    filters = {'user': user}
    if task:
        filters['task'] = task

    timers = Timer.objects.filter(**filters)
    total_seconds = 0
    for timer in timers:
        elapsed = timer.get_elapsed_time()
        # Debug print
        print(f"Timer for task '{timer.task.title}': elapsed {elapsed} seconds")
        total_seconds += elapsed

    # Debug print
    print(f"Total elapsed seconds for task '{task}': {total_seconds}")
    return total_seconds


@login_required
def home(request):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    todays_tasks = Task.objects.filter(user=request.user, deadline=today)
    upcoming_tasks = Task.objects.filter(user=request.user, deadline__gt=today).order_by('deadline')[:5]

    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()

    total_estimated_minutes = sum(
        (task.estimated_time or 0) for task in Task.objects.filter(user=request.user)
    )

    task_ids = []
    task_names = []
    estimated_minutes = []
    actual_minutes = []

    tasks_with_estimate = Task.objects.filter(user=request.user, estimated_time__isnull=False)
    for task in tasks_with_estimate:
        task_ids.append(str(task.id))  # convert to string for JS keys
        task_names.append(task.title)
        est = task.estimated_time or 0
        estimated_minutes.append(est)

        total_sec = get_total_elapsed_seconds(request.user, task=task)
        actual_minutes.append(total_sec / 60)  # convert seconds to minutes

    today_seconds = Timer.objects.filter(
        user=request.user,
        start_time__date=today
    ).aggregate(total=Sum('elapsed_time'))['total'] or 0

    week_seconds = Timer.objects.filter(
        user=request.user,
        start_time__date__range=(week_start, week_end)
    ).aggregate(total=Sum('elapsed_time'))['total'] or 0

    def seconds_to_hms(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h}h {m}m {s}s"

    context = {
        "todays_tasks": todays_tasks,
        "upcoming_tasks": upcoming_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_estimated_minutes": total_estimated_minutes,
        "task_ids": json.dumps(task_ids),
        "task_names": json.dumps(task_names),
        "estimated_minutes": json.dumps(estimated_minutes),
        "actual_minutes": json.dumps(actual_minutes),
        "today_time_str": seconds_to_hms(today_seconds),
        "week_time_str": seconds_to_hms(week_seconds),
    }
    return render(request, "dashboard/dashboard.html", context)
