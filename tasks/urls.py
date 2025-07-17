from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),  # ← updated this line
    path('daily/', views.daily_tasks, name='daily_tasks'),
    path('weekly/', views.weekly_tasks, name='weekly_tasks'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle_complete/<int:task_id>/', views.toggle_task_complete, name='toggle_task_complete'),
]
