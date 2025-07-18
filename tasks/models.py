from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    date = models.DateField(default=date.today) 
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    goal_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    category_color = models.CharField(max_length=7, default='#000000') 
    completed = models.BooleanField(default=False)
    estimated_time = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
