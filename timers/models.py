from django.db import models
from django.utils import timezone
from tasks.models import Task

class Timer(models.Model):
    POMODORO_WORK = 25 * 60  # 25 minutes in seconds
    POMODORO_SHORT_BREAK = 5 * 60  # 5 minutes in seconds
    POMODORO_LONG_BREAK = 15 * 60  # 15 minutes in seconds
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    start_time = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.IntegerField(default=0, help_text="Elapsed time in seconds")
    is_running = models.BooleanField(default=False)
    is_pomodoro = models.BooleanField(default=True)
    pomodoro_count = models.IntegerField(default=0)
    is_break = models.BooleanField(default=False)
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

    def get_remaining_time(self):
        if self.is_pomodoro:
            if self.is_break:
                target = self.POMODORO_LONG_BREAK if self.pomodoro_count % 4 == 0 else self.POMODORO_SHORT_BREAK
            else:
                target = self.POMODORO_WORK
            return max(0, target - self.get_elapsed_time())
        return 0

    def complete_pomodoro(self):
        self.pause()
        if not self.is_break:
            self.pomodoro_count += 1
        self.elapsed_time = 0
        self.is_break = not self.is_break
        self.save()

    def __str__(self):
        return f"Timer for {self.task} ({self.get_elapsed_time()}s)"