from django.contrib import admin
from events.models import Event, Participant, Attendance


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'max_capacity', 'created_at']
    search_fields = ['name', 'location']
    list_filter = ['date']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['event', 'participant', 'registered_at']
    list_filter = ['event', 'registered_at']
    search_fields = ['event__name', 'participant__name']