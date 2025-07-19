from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return ''

@register.filter
def seconds_to_hms(value):
    try:
        total_seconds = int(value)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}h {minutes}m {seconds}s"
    except (TypeError, ValueError):
        return ''

@register.filter
def minutes_to_hms(value):
    try:
        total_seconds = int(value) * 60
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except (TypeError, ValueError):
        return ''

@register.filter
def seconds_to_hours(value):
    try:
        return int(value) // 3600
    except (TypeError, ValueError):
        return 0

@register.filter
def seconds_to_minutes(value):
    try:
        return (int(value) % 3600) // 60
    except (TypeError, ValueError):
        return 0

@register.filter
def seconds_to_seconds(value):
    try:
        return int(value) % 60
    except (TypeError, ValueError):
        return 0
