from django.contrib import admin
from .models import DailySummary, WeeklySummary

admin.site.register(DailySummary)
admin.site.register(WeeklySummary)
