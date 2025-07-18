from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.start_timer, name="start_timer"),
    path("pause/", views.pause_timer, name="pause_timer"),
    path("complete/", views.complete_pomodoro, name="complete_pomodoro"),
    path("status/<int:task_id>/", views.get_timer_status, name="timer_status"),
]