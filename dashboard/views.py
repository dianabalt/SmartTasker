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
        # Get elapsed time includes both running and stopped time
        elapsed = timer.get_elapsed_time()
        total_seconds += elapsed
        # Also add any completed duration
        total_seconds += timer.duration

    return total_seconds


@login_required
def home(request):
    # Helper function to format seconds as h:m:s
    def seconds_to_hms(seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h}h {m}m {s}s"
    
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    todays_tasks = Task.objects.filter(user=request.user, deadline=today)
    upcoming_tasks = Task.objects.filter(user=request.user, deadline__gt=today).order_by('deadline')[:5]

    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_completed=True).count()

    # Get all tasks for the user
    all_user_tasks = Task.objects.filter(user=request.user)
    
    # Calculate total estimated seconds from all tasks (estimated_time is in seconds)
    total_estimated_seconds = sum(
        (task.estimated_time or 0) for task in all_user_tasks
    )
    
    # Convert to hours, minutes, seconds format
    total_estimated_str = seconds_to_hms(total_estimated_seconds)

    task_ids = []
    task_names = []
    estimated_minutes = []
    actual_minutes = []

    # Get tasks with estimate time for the chart
    tasks_with_estimate = Task.objects.filter(user=request.user, estimated_time__isnull=False)
    for task in tasks_with_estimate:
        task_ids.append(str(task.id))  # convert to string for JS keys
        task_names.append(task.title)
        # estimated_time is in seconds, convert to minutes for the chart
        est_minutes = (task.estimated_time or 0) / 60
        estimated_minutes.append(est_minutes)

        total_sec = get_total_elapsed_seconds(request.user, task=task)
        actual_minutes.append(total_sec / 60)  # convert seconds to minutes

    # Get today's time spent (actual elapsed time from all timers)
    today_timers = Timer.objects.filter(
        user=request.user,
        created_at__date=today
    )
    today_seconds = 0
    for timer in today_timers:
        today_seconds += timer.get_elapsed_time()
        today_seconds += timer.duration

    # Get this week's time spent (actual elapsed time from all timers)
    week_timers = Timer.objects.filter(
        user=request.user,
        created_at__date__range=(week_start, week_end)
    )
    week_seconds = 0
    for timer in week_timers:
        week_seconds += timer.get_elapsed_time()
        week_seconds += timer.duration

    context = {
        "todays_tasks": todays_tasks,
        "upcoming_tasks": upcoming_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_estimated_time": total_estimated_str,
        "task_ids": json.dumps(task_ids),
        "task_names": json.dumps(task_names),
        "estimated_minutes": json.dumps(estimated_minutes),
        "actual_minutes": json.dumps(actual_minutes),
        "today_time_str": seconds_to_hms(today_seconds),
        "week_time_str": seconds_to_hms(week_seconds),
    }
    return render(request, "dashboard/dashboard.html", context)