from rest_framework import serializers
from events.models import Attendance
from .event_serializer import EventSerializer
from .participant_serializer import ParticipantSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source='event', read_only=True)
    participant_details = ParticipantSerializer(source='participant', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'event', 'participant', 'event_details', 'participant_details', 'registered_at']
        read_only_fields = ['id', 'registered_at']


class AttendanceCreateSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    participant_id = serializers.IntegerField()