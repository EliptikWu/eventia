import pytest
from unittest.mock import Mock, patch
from events.services.participant_service import ParticipantService
from events.models import Participant


@pytest.fixture
def participant_service():
    return ParticipantService()


@pytest.fixture
def mock_participant():
    participant = Mock(spec=Participant)
    participant.id = 1
    participant.name = "John Doe"
    participant.email = "john@example.com"
    return participant


class TestParticipantService:
    
    def test_get_all_participants(self, participant_service, mock_participant):
        with patch.object(participant_service.participant_repository, 'get_all', return_value=[mock_participant]):
            participants = participant_service.get_all_participants()
            assert len(participants) == 1
            assert participants[0].name == "John Doe"
    
    def test_get_participant_by_id_success(self, participant_service, mock_participant):
        with patch.object(participant_service.participant_repository, 'get_by_id', return_value=mock_participant):
            participant = participant_service.get_participant_by_id(1)
            assert participant.id == 1
            assert participant.name == "John Doe"
    
    def test_get_participant_by_id_not_found(self, participant_service):
        with patch.object(participant_service.participant_repository, 'get_by_id', return_value=None):
            with pytest.raises(ValueError, match="Participant not found"):
                participant_service.get_participant_by_id(999)
    
    def test_create_participant_success(self, participant_service, mock_participant):
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '1234567890'
        }
        with patch.object(participant_service.participant_repository, 'get_by_email', return_value=None):
            with patch.object(participant_service.participant_repository, 'create', return_value=mock_participant):
                participant = participant_service.create_participant(data)
                assert participant.name == "John Doe"
    
    def test_create_participant_duplicate_email(self, participant_service, mock_participant):
        data = {
            'name': 'Jane Doe',
            'email': 'john@example.com'
        }
        with patch.object(participant_service.participant_repository, 'get_by_email', return_value=mock_participant):
            with pytest.raises(ValueError, match="A participant with this email already exists"):
                participant_service.create_participant(data)
    
    def test_update_participant_success(self, participant_service, mock_participant):
        data = {'name': 'John Updated'}
        with patch.object(participant_service.participant_repository, 'update', return_value=mock_participant):
            participant = participant_service.update_participant(1, data)
            assert participant is not None
    
    def test_update_participant_not_found(self, participant_service):
        with patch.object(participant_service.participant_repository, 'update', return_value=None):
            with pytest.raises(ValueError, match="Participant not found"):
                participant_service.update_participant(999, {'name': 'Updated'})
    
    def test_delete_participant_success(self, participant_service):
        with patch.object(participant_service.participant_repository, 'delete', return_value=True):
            result = participant_service.delete_participant(1)
            assert result is True
    
    def test_delete_participant_not_found(self, participant_service):
        with patch.object(participant_service.participant_repository, 'delete', return_value=False):
            with pytest.raises(ValueError, match="Participant not found"):
                participant_service.delete_participant(999)