from django.core.cache import cache
from events.models import Participant


class ParticipantRepository:
    CACHE_KEY_PREFIX = 'participant'
    CACHE_TIMEOUT = 300

    def get_all(self):
        cache_key = f'{self.CACHE_KEY_PREFIX}_all'
        participants = cache.get(cache_key)
        
        if participants is None:
            participants = list(Participant.objects.all())
            cache.set(cache_key, participants, self.CACHE_TIMEOUT)
        
        return participants

    def get_by_id(self, participant_id):
        cache_key = f'{self.CACHE_KEY_PREFIX}_{participant_id}'
        participant = cache.get(cache_key)
        
        if participant is None:
            try:
                participant = Participant.objects.get(id=participant_id)
                cache.set(cache_key, participant, self.CACHE_TIMEOUT)
            except Participant.DoesNotExist:
                return None
        
        return participant

    def get_by_email(self, email):
        try:
            return Participant.objects.get(email=email)
        except Participant.DoesNotExist:
            return None

    def create(self, data):
        participant = Participant.objects.create(**data)
        self._clear_cache()
        return participant

    def update(self, participant_id, data):
        participant = self.get_by_id(participant_id)
        if participant is None:
            return None
        
        for key, value in data.items():
            setattr(participant, key, value)
        participant.save()
        
        self._clear_cache()
        cache.delete(f'{self.CACHE_KEY_PREFIX}_{participant_id}')
        
        return participant

    def delete(self, participant_id):
        participant = self.get_by_id(participant_id)
        if participant is None:
            return False
        
        participant.delete()
        self._clear_cache()
        cache.delete(f'{self.CACHE_KEY_PREFIX}_{participant_id}')
        
        return True

    def _clear_cache(self):
        cache.delete(f'{self.CACHE_KEY_PREFIX}_all')