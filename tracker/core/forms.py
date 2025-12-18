from django import forms
from django.forms import ModelForm
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']
