import pytest
from datetime import datetime
from django.core.cache import cache
from events.repositories.event_repository import EventRepository
from events.models import Event


@pytest.mark.django_db
class TestEventRepository:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        cache.clear()
        yield
        cache.clear()
    
    @pytest.fixture
    def event_repository(self):
        return EventRepository()
    
    @pytest.fixture
    def sample_event_data(self):
        return {
            'name': 'Integration Test Event',
            'description': 'Test Description',
            'date': datetime(2025, 12, 1, 10, 0, 0),
            'location': 'Test Location',
            'max_capacity': 100
        }
    
    def test_create_event(self, event_repository, sample_event_data):
        event = event_repository.create(sample_event_data)
        
        assert event.id is not None
        assert event.name == 'Integration Test Event'
        assert event.max_capacity == 100
    
    def test_get_by_id(self, event_repository, sample_event_data):
        created_event = event_repository.create(sample_event_data)
        
        retrieved_event = event_repository.get_by_id(created_event.id)
        
        assert retrieved_event is not None
        assert retrieved_event.id == created_event.id
        assert retrieved_event.name == 'Integration Test Event'
    
    def test_get_by_id_not_found(self, event_repository):
        event = event_repository.get_by_id(99999)
        assert event is None
    
    def test_get_all(self, event_repository, sample_event_data):
        event_repository.create(sample_event_data)
        event_repository.create({**sample_event_data, 'name': 'Second Event'})
        
        events = event_repository.get_all()
        
        assert len(events) >= 2
    
    def test_update_event(self, event_repository, sample_event_data):
        event = event_repository.create(sample_event_data)
        
        updated_event = event_repository.update(event.id, {'name': 'Updated Event'})
        
        assert updated_event.name == 'Updated Event'
        assert updated_event.max_capacity == 100
    
    def test_delete_event(self, event_repository, sample_event_data):
        event = event_repository.create(sample_event_data)
        
        result = event_repository.delete(event.id)
        
        assert result is True
        assert event_repository.get_by_id(event.id) is None
    
    def test_cache_on_get_by_id(self, event_repository, sample_event_data):
        event = event_repository.create(sample_event_data)
        
        # Primera llamada - desde DB
        event1 = event_repository.get_by_id(event.id)
        
        # Segunda llamada - desde cache
        event2 = event_repository.get_by_id(event.id)
        
        assert event1.id == event2.id