from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from datetime import date, timedelta
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@login_required
def daily_tasks(request):
    today = date.today()

    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()

    all_tasks = Task.objects.filter(date=today, user=request.user)

    if search_query:
        all_tasks = all_tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if category_filter:
        all_tasks = all_tasks.filter(category=category_filter)

    incomplete_tasks = all_tasks.filter(is_completed=False)
    completed_tasks = all_tasks.filter(is_completed=True)

    if request.method == 'POST' and 'task_id' not in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('daily_tasks')
    else:
        form = TaskForm()

    edit_forms = {task.id: TaskForm(instance=task) for task in all_tasks}
    categories = Task.objects.filter(user=request.user).exclude(category='').values_list('category', flat=True).distinct()

    return render(request, 'tasks/daily_tasks.html', {
        'today': today,
        'incomplete_tasks': incomplete_tasks,
        'completed_tasks': completed_tasks,
        'form': form,
        'edit_forms': edit_forms,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    })


@login_required
def weekly_tasks(request):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday

    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()

    all_tasks = Task.objects.filter(user=request.user, date__range=(start_of_week, end_of_week)).order_by('date')

    if search_query:
        all_tasks = all_tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    if category_filter:
        all_tasks = all_tasks.filter(category=category_filter)

    # Handle new task creation
    if request.method == 'POST' and 'task_id' not in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('weekly_tasks')
    else:
        form = TaskForm()

    # Group by day for incomplete tasks
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    tasks_by_day = {day: [] for day in weekdays}
    for task in all_tasks:
        if not task.is_completed:
            weekday_name = task.date.strftime('%A')
            tasks_by_day[weekday_name].append(task)

    edit_forms = {task.id: TaskForm(instance=task) for task in all_tasks}
    categories = Task.objects.filter(user=request.user).exclude(category='').values_list('category', flat=True).distinct()

    return render(request, 'tasks/weekly_tasks.html', {
        'start_date': start_of_week,
        'end_date': end_of_week,
        'tasks_by_day': tasks_by_day,
        'all_tasks': all_tasks,
        'form': form,
        'edit_forms': edit_forms,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    })


@require_POST
@login_required
def toggle_task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'daily_tasks'))


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
    return redirect(request.META.get('HTTP_REFERER', 'daily_tasks'))


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
    return redirect(request.META.get('HTTP_REFERER', 'daily_tasks'))

@login_required
def home(request):
    return render(request, 'tasks/home.html')

