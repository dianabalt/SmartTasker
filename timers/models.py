class Timer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timers')
    duration = models.IntegerField(help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
