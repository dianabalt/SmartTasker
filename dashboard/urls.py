from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    #path('refresh-time/', views.refresh_time, name='refresh_time')
]
