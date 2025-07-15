from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:timer_id>/', views.start_timer, name='start_timer'),
    path('pause/<int:timer_id>/', views.pause_timer, name='pause_timer'),
    path('stop/<int:timer_id>/', views.stop_timer, name='stop_timer'),
]

