import pytest
from django.core.cache import cache
from events.repositories.participant_repository import ParticipantRepository
from events.models import Participant


@pytest.mark.django_db
class TestParticipantRepository:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        cache.clear()
        yield
        cache.clear()
    
    @pytest.fixture
    def participant_repository(self):
        return ParticipantRepository()
    
    @pytest.fixture
    def sample_participant_data(self):
        return {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890'
        }
    
    def test_create_participant(self, participant_repository, sample_participant_data):
        participant = participant_repository.create(sample_participant_data)
        
        assert participant.id is not None
        assert participant.name == 'John Doe'
        assert participant.email == 'john.doe@example.com'
    
    def test_get_by_id(self, participant_repository, sample_participant_data):
        created_participant = participant_repository.create(sample_participant_data)
        
        retrieved_participant = participant_repository.get_by_id(created_participant.id)
        
        assert retrieved_participant is not None
        assert retrieved_participant.id == created_participant.id
        assert retrieved_participant.email == 'john.doe@example.com'
    
    def test_get_by_email(self, participant_repository, sample_participant_data):
        participant_repository.create(sample_participant_data)
        
        participant = participant_repository.get_by_email('john.doe@example.com')
        
        assert participant is not None
        assert participant.name == 'John Doe'
    
    def test_get_by_email_not_found(self, participant_repository):
        participant = participant_repository.get_by_email('notfound@example.com')
        assert participant is None
    
    def test_get_all(self, participant_repository, sample_participant_data):
        participant_repository.create(sample_participant_data)
        participant_repository.create({**sample_participant_data, 'email': 'jane@example.com'})
        
        participants = participant_repository.get_all()
        
        assert len(participants) >= 2
    
    def test_update_participant(self, participant_repository, sample_participant_data):
        participant = participant_repository.create(sample_participant_data)
        
        updated_participant = participant_repository.update(participant.id, {'name': 'Jane Doe'})
        
        assert updated_participant.name == 'Jane Doe'
        assert updated_participant.email == 'john.doe@example.com'
    
    def test_delete_participant(self, participant_repository, sample_participant_data):
        participant = participant_repository.create(sample_participant_data)
        
        result = participant_repository.delete(participant.id)
        
        assert result is True
        assert participant_repository.get_by_id(participant.id) is None