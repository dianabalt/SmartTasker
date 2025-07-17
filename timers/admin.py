# timers/admin.py

from django.contrib import admin
from .models import Timer

@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'duration', 'formatted_elapsed_time', 'is_running', 'is_completed', 'created_at')
    list_filter = ('is_running', 'is_completed', 'created_at', 'task__title')
    search_fields = ('task__title',)
    actions = ['mark_as_completed', 'reset_timers']

    def formatted_elapsed_time(self, obj):
        minutes, seconds = divmod(obj.elapsed_time, 60)
        return f"{minutes:02}:{seconds:02}"
    formatted_elapsed_time.short_description = "Elapsed Time"

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f"{updated} timer(s) marked as completed.")
    mark_as_completed.short_description = "Mark selected timers as completed"

    def reset_timers(self, request, queryset):
        updated = queryset.update(elapsed_time=0, is_running=False, is_completed=False)
        self.message_user(request, f"{updated} timer(s) reset.")
    reset_timers.short_description = "Reset selected timers"
