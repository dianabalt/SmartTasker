from django.db import models
from tasks.models import Task  # assumes Task model exists

class Timer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    duration = models.IntegerField(default=0, help_text="Time in seconds")
    is_active = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    paused_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Timer for {self.task} ({self.duration}s)"

