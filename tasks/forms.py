from django import forms
from .models import Task

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'deadline',
            'goal_date',
            'category',
            'category_color',
            'estimated_time',
        ]
        widgets = {
            'category_color': forms.TextInput(attrs={'type': 'color'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'goal_date': forms.DateInput(attrs={'type': 'date'}),
            'estimated_time': forms.NumberInput(attrs={'min': 0}),
        }
