from django.urls import path
from events.views import event_views, participant_views, attendance_views

urlpatterns = [
    # Event endpoints
    path('events/', event_views.event_list, name='event-list'),
    path('events/<int:pk>/', event_views.event_detail, name='event-detail'),
    path('events/<int:pk>/statistics/', event_views.event_statistics, name='event-statistics'),
    
    # Participant endpoints
    path('participants/', participant_views.participant_list, name='participant-list'),
    path('participants/<int:pk>/', participant_views.participant_detail, name='participant-detail'),
    
    # Attendance endpoints
    path('attendance/register/', attendance_views.register_attendance, name='attendance-register'),
    path('attendance/cancel/', attendance_views.cancel_attendance, name='attendance-cancel'),
    path('attendance/event/<int:event_id>/', attendance_views.event_attendees, name='event-attendees'),
    path('attendance/participant/<int:participant_id>/', attendance_views.participant_events, name='participant-events'),
]