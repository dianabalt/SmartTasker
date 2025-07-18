import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Timer
from tasks.models import Task

@csrf_exempt
def start_timer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        task = Task.objects.get(id=task_id)
        
        timer, created = Timer.objects.get_or_create(task=task, defaults={'is_pomodoro': True})
        timer.start()
        
        return JsonResponse({
            "status": "started",
            "remaining_time": timer.get_remaining_time(),
            "is_break": timer.is_break,
            "pomodoro_count": timer.pomodoro_count
        })

@csrf_exempt
def pause_timer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        task = Task.objects.get(id=task_id)
        
        timer = Timer.objects.filter(task=task).last()
        if timer:
            timer.pause()
        
        return JsonResponse({"status": "paused"})

@csrf_exempt
def complete_pomodoro(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        task = Task.objects.get(id=task_id)
        
        timer = Timer.objects.filter(task=task).last()
        if timer:
            timer.complete_pomodoro()
        
        return JsonResponse({
            "status": "completed",
            "is_break": timer.is_break,
            "pomodoro_count": timer.pomodoro_count
        })

@csrf_exempt
def get_timer_status(request, task_id):
    task = Task.objects.get(id=task_id)
    timer = Timer.objects.filter(task=task).last()
    
    if timer:
        return JsonResponse({
            "is_running": timer.is_running,
            "remaining_time": timer.get_remaining_time(),
            "elapsed_time": timer.get_elapsed_time(),
            "is_break": timer.is_break,
            "pomodoro_count": timer.pomodoro_count
        })
    
    return JsonResponse({"is_running": False, "remaining_time": 1500})