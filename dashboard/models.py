from django.db import models

class DailySummary(models.Model):
    date = models.DateField()
    total_time_spent = models.DurationField()
    productive_time = models.DurationField()
    unproductive_time = models.DurationField()

    estimated_time = models.DurationField(null=True, blank=True)
    actual_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Daily Summary for {self.date}"


class WeeklySummary(models.Model):
    week_start = models.DateField()
    week_end = models.DateField()
    total_time_spent = models.DurationField()
    average_daily_productive_time = models.DurationField()

    def __str__(self):
        return f"Weekly Summary ({self.week_start} - {self.week_end})"
