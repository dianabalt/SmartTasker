import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Timer
from tasks.models import Task

@csrf_exempt
@login_required
def start_timer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")
            if not task_id:
                return JsonResponse({"error": "Missing task_id"}, status=400)

            task = Task.objects.get(id=task_id, user=request.user)
            # Stop existing timers
            Timer.objects.filter(task=task, user=request.user, is_running=True).update(is_running=False)

            # Start a new timer
            Timer.objects.create(
                user=request.user,
                task=task,
                start_time=timezone.now(),
                is_running=True
            )

            return JsonResponse({"status": "started", "task_id": task_id})
        
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@login_required
def pause_timer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")

            if not task_id:
                return JsonResponse({"error": "Missing task_id"}, status=400)

            task = Task.objects.get(id=task_id, user=request.user)
            timer = Timer.objects.filter(task=task, user=request.user, is_running=True).last()

            if timer:
                elapsed = timezone.now() - timer.start_time
                timer.elapsed_time += int(elapsed.total_seconds())
                timer.is_running = False
                timer.save()

            return JsonResponse({"status": "paused", "task_id": task_id})

        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@login_required
def stop_timer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")

            if not task_id:
                return JsonResponse({"error": "Missing task_id"}, status=400)

            task = Task.objects.get(id=task_id, user=request.user)
            timer = Timer.objects.filter(task=task, user=request.user, is_running=True).last()

            if timer:
                elapsed = timezone.now() - timer.start_time
                timer.elapsed_time += int(elapsed.total_seconds())
                timer.is_running = False
                timer.save()

            return JsonResponse({"status": "stopped", "task_id": task_id})

        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

