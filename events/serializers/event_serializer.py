from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'location', 'max_capacity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_max_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Max capacity must be greater than 0")
        return value