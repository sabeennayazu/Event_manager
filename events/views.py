from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
import calendar
from .models import Event, Reminder
from .forms import EventForm, ReminderForm


def event_list(request):
    
    view_type = request.GET.get('view', 'month')
    today = timezone.now().date()
    
    if view_type == 'day':
        events = Event.objects.filter(date=today)
        context = {
            'events': events,
            'view_type': 'day',
            'current_date': today,
        }
    elif view_type == 'week':
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        events = Event.objects.filter(date__range=[start_week, end_week])
        context = {
            'events': events,
            'view_type': 'week',
            'start_week': start_week,
            'end_week': end_week,
        }
    else:  
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        
        first_day = datetime(year, month, 1).date()
        last_day = datetime(year, month, calendar.monthrange(year, month)[1]).date()
        
        events = Event.objects.filter(date__range=[first_day, last_day])
        
       
        cal = calendar.monthcalendar(year, month)
        events_by_date = {}
        for event in events:
            if event.date not in events_by_date:
                events_by_date[event.date] = []
            events_by_date[event.date].append(event)
        
        context = {
            'events': events,
            'view_type': 'month',
            'calendar': cal,
            'events_by_date': events_by_date,
            'current_month': month,
            'current_year': year,
            'month_name': calendar.month_name[month],
            'prev_month': month - 1 if month > 1 else 12,
            'next_month': month + 1 if month < 12 else 1,
            'prev_year': year if month > 1 else year - 1,
            'next_year': year if month < 12 else year + 1,
        }
    
    return render(request, 'events/event_list.html', context)


def add_event(request):
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" has been created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/add_event.html', {'form': form})


def edit_event(request, event_id):
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.title}" has been updated successfully!')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


def delete_event(request, event_id):
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" has been deleted successfully!')
        return redirect('event_list')
    
    return render(request, 'events/delete_event.html', {'event': event})


def mark_attended(request, event_id):
    # jati garera ni namilesi ai nai use garna paryo yesma
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.is_attended = not event.is_attended
        event.save()
        
        status = "attended" if event.is_attended else "not attended"
        messages.success(request, f'Event "{event.title}" marked as {status}!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_attended': event.is_attended,
                'message': f'Event marked as {status}!'
            })
    
    return redirect('event_list')


def set_reminder(request, event_id):
    "
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.event = event
            try:
                reminder.save()
                messages.success(request, f'Reminder set for "{event.title}"!')
                return redirect('event_detail', event_id=event.id)
            except:
                messages.error(request, 'A reminder with this timing already exists for this event.')
    else:
        form = ReminderForm()
    
    return render(request, 'events/set_reminder.html', {'form': form, 'event': event})


def event_detail(request, event_id):
   
    event = get_object_or_404(Event, id=event_id)
    reminders = event.reminders.all()
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'reminders': reminders
    })


def delete_reminder(request, reminder_id):
    
    reminder = get_object_or_404(Reminder, id=reminder_id)
    event_id = reminder.event.id
    
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Reminder deleted successfully!')
    
    return redirect('event_detail', event_id=event_id)
