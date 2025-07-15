from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),       
    path('dashboard/', include('dashboard.urls')), 
    path('accounts/', include('accounts.urls')),    
    path('timers/', include('timers.urls')),     
]
