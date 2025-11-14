from rest_framework import serializers
from events.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        if self.instance is None:
            if Participant.objects.filter(email=value).exists():
                raise serializers.ValidationError("A participant with this email already exists")
        else:
            if Participant.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A participant with this email already exists")
        return value