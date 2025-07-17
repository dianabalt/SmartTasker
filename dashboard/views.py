from django.shortcuts import render
from .models import DailySummary
from datetime import date


def home(request):
    today = date.today()
    try:
        summary = DailySummary.objects.get(date=today)
    except DailySummary.DoesNotExist:
        summary = None

    context = {
        "summary": summary,
    }
    return render(request, "dashboard/home.html", context)
