from django import forms
from .models import Event, Reminder


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'time', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter event description (optional)'
            }),
        }


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['reminder_type', 'minutes_before']
        widgets = {
            'reminder_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'minutes_before': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
