from django.contrib import admin
from .models import Timer

@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'formatted_elapsed_time', 'is_running', 'is_pomodoro', 'pomodoro_count', 'is_break', 'created_at')
    list_filter = ('is_running', 'is_pomodoro', 'is_break', 'created_at')
    search_fields = ('task__title',)

    def formatted_elapsed_time(self, obj):
        minutes, seconds = divmod(obj.elapsed_time, 60)
        return f"{minutes:02}:{seconds:02}"
    formatted_elapsed_time.short_description = "Elapsed Time"