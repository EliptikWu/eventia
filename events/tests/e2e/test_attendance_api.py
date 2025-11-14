import pytest
from datetime import datetime
from rest_framework.test import APIClient
from django.urls import reverse
from events.models import Event, Participant, Attendance


@pytest.mark.django_db
class TestAttendanceAPI:
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def sample_event(self):
        return Event.objects.create(
            name='Test Event',
            description='Description',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=50
        )
    
    @pytest.fixture
    def sample_participant(self):
        return Participant.objects.create(
            name='John Doe',
            email='john.attendance@example.com',
            phone='1234567890'
        )
    
    def test_register_attendance(self, api_client, sample_event, sample_participant):
        url = reverse('attendance-register')
        data = {
            'event_id': sample_event.id,
            'participant_id': sample_participant.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 201
        assert response.data['event'] == sample_event.id
        assert response.data['participant'] == sample_participant.id
    
    def test_register_attendance_duplicate(self, api_client, sample_event, sample_participant):
        Attendance.objects.create(event=sample_event, participant=sample_participant)
        
        url = reverse('attendance-register')
        data = {
            'event_id': sample_event.id,
            'participant_id': sample_participant.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 400
        assert 'already registered' in response.data['error']
    
    def test_register_attendance_full_capacity(self, api_client, sample_participant):
        event = Event.objects.create(
            name='Full Event',
            description='Description',
            date=datetime(2025, 12, 1, 10, 0, 0),
            location='Location',
            max_capacity=1
        )
        
        other_participant = Participant.objects.create(
            name='Other',
            email='other@example.com'
        )
        Attendance.objects.create(event=event, participant=other_participant)
        
        url = reverse('attendance-register')
        data = {
            'event_id': event.id,
            'participant_id': sample_participant.id
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 400
        assert 'full capacity' in response.data['error']
    
    def test_cancel_attendance(self, api_client, sample_event, sample_participant):
        Attendance.objects.create(event=sample_event, participant=sample_participant)
        
        url = reverse('attendance-cancel')
        data = {
            'event_id': sample_event.id,
            'participant_id': sample_participant.id
        }
        response = api_client.delete(url, data, format='json')
        
        assert response.status_code == 204
    
    def test_get_event_attendees(self, api_client, sample_event, sample_participant):
        Attendance.objects.create(event=sample_event, participant=sample_participant)
        
        url = reverse('event-attendees', kwargs={'event_id': sample_event.id})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) >= 1
    
    def test_get_participant_events(self, api_client, sample_event, sample_participant):
        Attendance.objects.create(event=sample_event, participant=sample_participant)
        
        url = reverse('participant-events', kwargs={'participant_id': sample_participant.id})
        response = api_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) >= 1