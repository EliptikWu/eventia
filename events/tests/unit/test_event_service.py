import pytest
from unittest.mock import Mock, patch
from events.services.event_service import EventService
from events.models import Event


@pytest.fixture
def event_service():
    return EventService()


@pytest.fixture
def mock_event():
    event = Mock(spec=Event)
    event.id = 1
    event.name = "Test Event"
    event.max_capacity = 100
    return event


class TestEventService:
    
    def test_get_all_events(self, event_service, mock_event):
        with patch.object(event_service.event_repository, 'get_all', return_value=[mock_event]):
            events = event_service.get_all_events()
            assert len(events) == 1
            assert events[0].name == "Test Event"
    
    def test_get_event_by_id_success(self, event_service, mock_event):
        with patch.object(event_service.event_repository, 'get_by_id', return_value=mock_event):
            event = event_service.get_event_by_id(1)
            assert event.id == 1
            assert event.name == "Test Event"
    
    def test_get_event_by_id_not_found(self, event_service):
        with patch.object(event_service.event_repository, 'get_by_id', return_value=None):
            with pytest.raises(ValueError, match="Event not found"):
                event_service.get_event_by_id(999)
    
    def test_create_event_success(self, event_service, mock_event):
        data = {
            'name': 'New Event',
            'description': 'Description',
            'date': '2025-12-01T10:00:00Z',
            'location': 'Test Location',
            'max_capacity': 50
        }
        with patch.object(event_service.event_repository, 'create', return_value=mock_event):
            event = event_service.create_event(data)
            assert event.name == "Test Event"
    
    def test_create_event_invalid_capacity(self, event_service):
        data = {
            'name': 'New Event',
            'max_capacity': 0
        }
        with pytest.raises(ValueError, match="Max capacity must be greater than 0"):
            event_service.create_event(data)
    
    def test_update_event_success(self, event_service, mock_event):
        data = {'name': 'Updated Event'}
        with patch.object(event_service.event_repository, 'update', return_value=mock_event):
            event = event_service.update_event(1, data)
            assert event is not None
    
    def test_update_event_not_found(self, event_service):
        with patch.object(event_service.event_repository, 'update', return_value=None):
            with pytest.raises(ValueError, match="Event not found"):
                event_service.update_event(999, {'name': 'Updated'})
    
    def test_delete_event_success(self, event_service):
        with patch.object(event_service.event_repository, 'delete', return_value=True):
            result = event_service.delete_event(1)
            assert result is True
    
    def test_delete_event_not_found(self, event_service):
        with patch.object(event_service.event_repository, 'delete', return_value=False):
            with pytest.raises(ValueError, match="Event not found"):
                event_service.delete_event(999)
    
    def test_get_event_statistics(self, event_service, mock_event):
        with patch.object(event_service.event_repository, 'get_by_id', return_value=mock_event):
            with patch.object(event_service.attendance_repository, 'count_by_event', return_value=75):
                stats = event_service.get_event_statistics(1)
                assert stats['event_id'] == 1
                assert stats['event_name'] == "Test Event"
                assert stats['max_capacity'] == 100
                assert stats['total_attendees'] == 75
                assert stats['available_capacity'] == 25
                assert stats['occupancy_percentage'] == 75.0
                assert stats['is_full'] is False