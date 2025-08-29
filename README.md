# Event Manager

A Django-based web application for organizing and managing events. Users can add events, mark them as attended, set reminders, and view events by day, week, or month.

## Features

- **Event Management**: Add, edit, and delete events with title, date, time, and description
- **Attendance Tracking**: Mark events as attended or not attended
- **Reminder System**: Set multiple reminders for events (5 minutes to 1 week before)
- **Multiple Views**: View events by day, week, or month with an interactive calendar
- **Responsive Design**: Modern, mobile-friendly interface using Bootstrap 5
- **AJAX Functionality**: Mark attendance without page reload

## Models

### Event
- `title`: Event title (max 100 characters)
- `date`: Event date
- `time`: Optional event time
- `description`: Optional event description
- `is_attended`: Boolean flag for attendance status
- `created_at`: Timestamp when event was created
- `updated_at`: Timestamp when event was last modified

### Reminder
- `event`: Foreign key to Event
- `reminder_type`: Email or Notification
- `minutes_before`: Time before event (5 min to 1 week)
- `is_sent`: Boolean flag for reminder status

## Installation

1. **Clone or download the project**
   ```bash
   cd "event manager"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000`

## Usage

### Adding Events
1. Click "Add Event" in the navigation bar
2. Fill in the event details (title and date are required)
3. Optionally add time and description
4. Click "Save Event"

### Viewing Events
- **Day View**: Shows today's events
- **Week View**: Shows current week's events
- **Month View**: Interactive calendar showing all events for the month

### Managing Events
- Click on any event to view details
- Edit events by clicking the edit button
- Mark events as attended/not attended
- Delete events when no longer needed

### Setting Reminders
1. Go to an event's detail page
2. Click "Add Reminder"
3. Choose reminder type and timing
4. Multiple reminders can be set for each event

## Views

- `event_list`: List all events with filtering by day/week/month
- `add_event`: Add a new event
- `edit_event`: Edit an existing event
- `delete_event`: Delete an event
- `event_detail`: View event details and reminders
- `mark_attended`: Toggle attendance status
- `set_reminder`: Add reminders to events

## Technologies Used

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, Font Awesome icons
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **JavaScript**: Vanilla JS with AJAX for dynamic interactions

## File Structure

```
event_manager/
├── event_manager/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/                 # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/                 # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/              # HTML templates
│   ├── base.html
│   └── events/
│       ├── add_event.html
│       ├── delete_event.html
│       ├── edit_event.html
│       ├── event_detail.html
│       ├── event_list.html
│       └── set_reminder.html
├── manage.py
├── requirements.txt
└── README.md
```

## Customization

### Adding New Reminder Types
Edit the `REMINDER_TYPES` in `events/models.py`:
```python
REMINDER_TYPES = [
    ('email', 'Email'),
    ('notification', 'Notification'),
    ('sms', 'SMS'),  # Add new type
]
```

### Changing Time Zone
Update `TIME_ZONE` in `event_manager/settings.py`:
```python
TIME_ZONE = 'Your/Timezone'  # e.g., 'America/New_York'
```

### Styling
Modify `static/css/style.css` to customize the appearance.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the project repository.
