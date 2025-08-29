from django.contrib import admin
from .models import Event, Reminder


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'is_attended', 'created_at']
    list_filter = ['is_attended', 'date', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'
    ordering = ['date', 'time']


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['event', 'reminder_type', 'minutes_before', 'is_sent', 'created_at']
    list_filter = ['reminder_type', 'minutes_before', 'is_sent']
    search_fields = ['event__title']
