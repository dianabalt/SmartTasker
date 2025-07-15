from django.db import models
from tasks.models import Task  

class Timer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    duration = models.IntegerField(help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Timer for {self.task} ({self.duration}s)"

