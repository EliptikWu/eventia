import pytest
from datetime import datetime
from rest_framework.test import APIClient
from django.urls import reverse
from events.models import Event


@pytest.mark.django_db
class TestEventAPI:
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def sample_event_data(self):
        return {
            'name': 'API Test Event',
            'description': 'Test Description',
            'date': '2025-12-01T10:00:00Z',
            'location': 'Test Location',
            'max_capacity': 50
        }
    
    def test_create_event(self, api_client, sample_event_data):
        url = reverse('event-list')
        response = api_client.post(url, sample_event_data, format='json')
        
        assert response.status_code == 201
        assert response.data['name'] == 'API Test Event'
        assert response.data['max_capacity'] == 50
    
    def test_create_event_invalid_capacity(self, api_client, sample_event_data):
        sample_event_data['max_capacity'] = 0
        url = reverse('event-list')
        response = api_client.post(url, sample_event_data, format='json')
        
        assert response.status_code == 400
    
    def test_get_all_events(self, api_client, sample_event_data):
        Event.objects.create(
            name='Event 1',
            description='Desc',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=100
        )
        
        url = reverse('event-list')
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) >= 1
    
    def test_get_event_by_id(self, api_client):
        event = Event.objects.create(
            name='Single Event',
            description='Desc',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=100
        )
        
        url = reverse('event-detail', kwargs={'pk': event.id})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert response.data['name'] == 'Single Event'
    
    def test_update_event(self, api_client):
        event = Event.objects.create(
            name='Old Name',
            description='Desc',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=100
        )
        
        url = reverse('event-detail', kwargs={'pk': event.id})
        response = api_client.put(url, {'name': 'New Name'}, format='json')
        
        assert response.status_code == 200
        assert response.data['name'] == 'New Name'
    
    def test_delete_event(self, api_client):
        event = Event.objects.create(
            name='To Delete',
            description='Desc',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=100
        )
        
        url = reverse('event-detail', kwargs={'pk': event.id})
        response = api_client.delete(url)
        
        assert response.status_code == 204
        assert Event.objects.filter(id=event.id).count() == 0
    
    def test_get_event_statistics(self, api_client):
        event = Event.objects.create(
            name='Stats Event',
            description='Desc',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=100
        )
        
        url = reverse('event-statistics', kwargs={'pk': event.id})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert 'max_capacity' in response.data
        assert 'total_attendees' in response.data
        assert 'occupancy_percentage' in response.data