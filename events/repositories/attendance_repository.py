from django.core.cache import cache
from events.models import Attendance


class AttendanceRepository:
    CACHE_KEY_PREFIX = 'attendance'
    CACHE_TIMEOUT = 300

    def get_by_event(self, event_id):
        cache_key = f'{self.CACHE_KEY_PREFIX}_event_{event_id}'
        attendances = cache.get(cache_key)
        
        if attendances is None:
            attendances = list(Attendance.objects.filter(event_id=event_id).select_related('participant'))
            cache.set(cache_key, attendances, self.CACHE_TIMEOUT)
        
        return attendances

    def get_by_participant(self, participant_id):
        return Attendance.objects.filter(participant_id=participant_id).select_related('event')

    def get_by_event_and_participant(self, event_id, participant_id):
        try:
            return Attendance.objects.get(event_id=event_id, participant_id=participant_id)
        except Attendance.DoesNotExist:
            return None

    def count_by_event(self, event_id):
        cache_key = f'{self.CACHE_KEY_PREFIX}_count_{event_id}'
        count = cache.get(cache_key)
        
        if count is None:
            count = Attendance.objects.filter(event_id=event_id).count()
            cache.set(cache_key, count, self.CACHE_TIMEOUT)
        
        return count

    def create(self, event_id, participant_id):
        attendance = Attendance.objects.create(event_id=event_id, participant_id=participant_id)
        self._clear_event_cache(event_id)
        return attendance

    def delete(self, event_id, participant_id):
        attendance = self.get_by_event_and_participant(event_id, participant_id)
        if attendance is None:
            return False
        
        attendance.delete()
        self._clear_event_cache(event_id)
        
        return True

    def _clear_event_cache(self, event_id):
        cache.delete(f'{self.CACHE_KEY_PREFIX}_event_{event_id}')
        cache.delete(f'{self.CACHE_KEY_PREFIX}_count_{event_id}')