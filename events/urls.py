from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('add/', views.add_event, name='add_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/mark-attended/', views.mark_attended, name='mark_attended'),
    path('event/<int:event_id>/set-reminder/', views.set_reminder, name='set_reminder'),
    path('reminder/<int:reminder_id>/delete/', views.delete_reminder, name='delete_reminder'),
]
