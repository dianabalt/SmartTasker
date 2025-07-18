from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tasks.models import Task

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    duration = models.IntegerField(help_text="Duration in seconds", default=0)  # total duration (optional)
    start_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(default=0, help_text="Elapsed time in seconds")
    is_running = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def start(self):
        if not self.is_running:
            self.start_time = timezone.now()
            self.is_running = True
            self.save()

    def pause(self):
        if self.is_running and self.start_time:
            now = timezone.now()
            self.elapsed_time += int((now - self.start_time).total_seconds())
            self.start_time = None
            self.is_running = False
            self.save()

    def get_elapsed_time(self):
        if self.is_running and self.start_time:
            now = timezone.now()
            return self.elapsed_time + int((now - self.start_time).total_seconds())
        return self.elapsed_time

    def stop(self):
        self.pause()
        total = self.elapsed_time
        self.duration = total
        self.elapsed_time = 0
        self.save()
        return total

    def __str__(self):
        return f"Timer for {self.task} ({self.get_elapsed_time()}s)"

