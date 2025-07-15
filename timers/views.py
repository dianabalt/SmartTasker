from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Timer
from django.utils.timezone import now

def start_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    timer.is_active = True
    timer.is_paused = False
    timer.started_at = now()
    timer.save()
    return JsonResponse({'status': 'started'})

def pause_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    if timer.is_active and not timer.is_paused:
        timer.is_paused = True
        timer.paused_at = now()
        # Optionally calculate time spent so far
        timer.save()
    return JsonResponse({'status': 'paused'})

def stop_timer(request, timer_id):
    timer = get_object_or_404(Timer, id=timer_id)
    timer.is_active = False
    timer.is_paused = False
    # Optionally finalize time tracking
    timer.save()
    return JsonResponse({'status': 'stopped'})

