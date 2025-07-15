from django.db import models
from tasks.models import Task
from django.contrib.auth.models import User

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0, help_text="Accumulated time in seconds")
    is_active = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Timer for {self.task.title} - {self.duration}s"
