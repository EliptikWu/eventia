from django.core.cache import cache
from events.models import Event


class EventRepository:
    CACHE_KEY_PREFIX = 'event'
    CACHE_TIMEOUT = 300  # 5 minutos

    def get_all(self):
        cache_key = f'{self.CACHE_KEY_PREFIX}_all'
        events = cache.get(cache_key)
        
        if events is None:
            events = list(Event.objects.all())
            cache.set(cache_key, events, self.CACHE_TIMEOUT)
        
        return events

    def get_by_id(self, event_id):
        cache_key = f'{self.CACHE_KEY_PREFIX}_{event_id}'
        event = cache.get(cache_key)
        
        if event is None:
            try:
                event = Event.objects.get(id=event_id)
                cache.set(cache_key, event, self.CACHE_TIMEOUT)
            except Event.DoesNotExist:
                return None
        
        return event

    def create(self, data):
        event = Event.objects.create(**data)
        self._clear_cache()
        return event

    def update(self, event_id, data):
        event = self.get_by_id(event_id)
        if event is None:
            return None
        
        for key, value in data.items():
            setattr(event, key, value)
        event.save()
        
        self._clear_cache()
        cache.delete(f'{self.CACHE_KEY_PREFIX}_{event_id}')
        
        return event

    def delete(self, event_id):
        event = self.get_by_id(event_id)
        if event is None:
            return False
        
        event.delete()
        self._clear_cache()
        cache.delete(f'{self.CACHE_KEY_PREFIX}_{event_id}')
        
        return True

    def _clear_cache(self):
        cache.delete(f'{self.CACHE_KEY_PREFIX}_all')