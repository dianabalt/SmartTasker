from django.utils import timezone
from django.shortcuts import render
from datetime import date, timedelta
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tasks.models import Task
from timers.models import Timer


def get_total_elapsed_seconds(user, task=None):
    filters = {'user': user}
    if task:
        filters['task'] = task

    timers = Timer.objects.filter(**filters)
    total_seconds = 0
    for timer in timers:
        total_seconds += timer.get_elapsed_time()

    return total_seconds


@login_required
def home(request):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Fetch tasks
    todays_tasks = Task.objects.filter(user=request.user, deadline=today)
    upcoming_tasks = Task.objects.filter(user=request.user, deadline__gt=today).order_by('deadline')[:5]

    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()

    # Total estimated seconds (from all tasks)
    total_estimated_seconds = sum(
        (task.estimated_time or 0) for task in Task.objects.filter(user=request.user)
    )
    total_estimated_minutes = total_estimated_seconds / 60 if total_estimated_seconds else 0

    # Per-task estimated and actual minutes
    task_ids = []
    task_names = []
    estimated_minutes = []
    actual_minutes = []

    tasks_with_estimate = Task.objects.filter(user=request.user, estimated_time__isnull=False)
    for task in tasks_with_estimate:
        task_ids.append(str(task.id))
        task_names.append(task.title)
        est_seconds = task.estimated_time or 0
        estimated_minutes.append(est_seconds / 60)  # convert to minutes

        actual_sec = get_total_elapsed_seconds(request.user, task=task)
        actual_minutes.append(actual_sec / 60)  # convert to minutes

    # Total seconds for today (all timers started/created today)
    today_timers = Timer.objects.filter(user=request.user, created_at__date=today)
    today_seconds = sum(timer.get_elapsed_time() for timer in today_timers)

    # Total seconds for week (all timers started/created this week)
    week_timers = Timer.objects.filter(user=request.user, created_at__date__range=(week_start, week_end))
    week_seconds = sum(timer.get_elapsed_time() for timer in week_timers)

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


@login_required
def refresh_time(request):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    today_timers = Timer.objects.filter(user=request.user, created_at__date=today)
    today_seconds = sum(timer.get_elapsed_time() for timer in today_timers)

    week_timers = Timer.objects.filter(user=request.user, created_at__date__range=(week_start, week_end))
    week_seconds = sum(timer.get_elapsed_time() for timer in week_timers)

    def seconds_to_hms(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h}h {m}m {s}s"

    return JsonResponse({
        'today_time': seconds_to_hms(today_seconds),
        'week_time': seconds_to_hms(week_seconds)
    })
