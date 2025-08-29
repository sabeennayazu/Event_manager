from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"

    @property
    def is_past(self):
        return self.date < timezone.now().date()

    @property
    def is_today(self):
        return self.date == timezone.now().date()


class Reminder(models.Model):
    REMINDER_TYPES = [
        ('email', 'Email'),
        ('notification', 'Notification'),
    ]
    
    REMINDER_TIMES = [
        (5, '5 minutes before'),
        (15, '15 minutes before'),
        (30, '30 minutes before'),
        (60, '1 hour before'),
        (1440, '1 day before'),
        (10080, '1 week before'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES, default='notification')
    minutes_before = models.IntegerField(choices=REMINDER_TIMES, default=15)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'minutes_before']

    def __str__(self):
        return f"Reminder for {self.event.title} - {self.get_minutes_before_display()}"

    @property
    def reminder_time(self):
        if self.event.time:
            event_datetime = datetime.combine(self.event.date, self.event.time)
        else:
            event_datetime = datetime.combine(self.event.date, datetime.min.time())
        return event_datetime - timedelta(minutes=self.minutes_before)
