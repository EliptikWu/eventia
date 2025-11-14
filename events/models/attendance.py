from django.db import models
from .event import Event
from .participant import Participant


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='attendances')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendances'
        unique_together = ['event', 'participant']
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.participant.name} - {self.event.name}"