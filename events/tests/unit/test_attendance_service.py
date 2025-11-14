import pytest
from unittest.mock import Mock, patch
from events.services.attendance_service import AttendanceService
from events.models import Event, Participant, Attendance


@pytest.fixture
def attendance_service():
    return AttendanceService()


@pytest.fixture
def mock_event():
    event = Mock(spec=Event)
    event.id = 1
    event.max_capacity = 100
    return event


@pytest.fixture
def mock_participant():
    participant = Mock(spec=Participant)
    participant.id = 1
    return participant


@pytest.fixture
def mock_attendance():
    attendance = Mock(spec=Attendance)
    attendance.id = 1
    attendance.event_id = 1
    attendance.participant_id = 1
    return attendance


class TestAttendanceService:
    
    def test_register_attendance_success(self, attendance_service, mock_event, mock_participant, mock_attendance):
        with patch.object(attendance_service.event_repository, 'get_by_id', return_value=mock_event):
            with patch.object(attendance_service.participant_repository, 'get_by_id', return_value=mock_participant):
                with patch.object(attendance_service.attendance_repository, 'get_by_event_and_participant', return_value=None):
                    with patch.object(attendance_service.attendance_repository, 'count_by_event', return_value=50):
                        with patch.object(attendance_service.attendance_repository, 'create', return_value=mock_attendance):
                            attendance = attendance_service.register_attendance(1, 1)
                            assert attendance.id == 1
    
    def test_register_attendance_event_not_found(self, attendance_service):
        with patch.object(attendance_service.event_repository, 'get_by_id', return_value=None):
            with pytest.raises(ValueError, match="Event not found"):
                attendance_service.register_attendance(1, 1)
    
    def test_register_attendance_participant_not_found(self, attendance_service, mock_event):
        with patch.object(attendance_service.event_repository, 'get_by_id', return_value=mock_event):
            with patch.object(attendance_service.participant_repository, 'get_by_id', return_value=None):
                with pytest.raises(ValueError, match="Participant not found"):
                    attendance_service.register_attendance(1, 1)
    
    def test_register_attendance_already_registered(self, attendance_service, mock_event, mock_participant, mock_attendance):
        with patch.object(attendance_service.event_repository, 'get_by_id', return_value=mock_event):
            with patch.object(attendance_service.participant_repository, 'get_by_id', return_value=mock_participant):
                with patch.object(attendance_service.attendance_repository, 'get_by_event_and_participant', return_value=mock_attendance):
                    with pytest.raises(ValueError, match="Participant is already registered for this event"):
                        attendance_service.register_attendance(1, 1)
    
    def test_register_attendance_full_capacity(self, attendance_service, mock_event, mock_participant):
        with patch.object(attendance_service.event_repository, 'get_by_id', return_value=mock_event):
            with patch.object(attendance_service.participant_repository, 'get_by_id', return_value=mock_participant):
                with patch.object(attendance_service.attendance_repository, 'get_by_event_and_participant', return_value=None):
                    with patch.object(attendance_service.attendance_repository, 'count_by_event', return_value=100):
                        with pytest.raises(ValueError, match="Event is at full capacity"):
                            attendance_service.register_attendance(1, 1)
    
    def test_cancel_attendance_success(self, attendance_service):
        with patch.object(attendance_service.attendance_repository, 'delete', return_value=True):
            result = attendance_service.cancel_attendance(1, 1)
            assert result is True
    
    def test_cancel_attendance_not_found(self, attendance_service):
        with patch.object(attendance_service.attendance_repository, 'delete', return_value=False):
            with pytest.raises(ValueError, match="Attendance record not found"):
                attendance_service.cancel_attendance(1, 1)
    
    def test_get_attendees_by_event(self, attendance_service, mock_event, mock_attendance):
        with patch.object(attendance_service.event_repository, 'get_by_id', return_value=mock_event):
            with patch.object(attendance_service.attendance_repository, 'get_by_event', return_value=[mock_attendance]):
                attendances = attendance_service.get_attendees_by_event(1)
                assert len(attendances) == 1
    
    def test_get_events_by_participant(self, attendance_service, mock_participant, mock_attendance):
        with patch.object(attendance_service.participant_repository, 'get_by_id', return_value=mock_participant):
            with patch.object(attendance_service.attendance_repository, 'get_by_participant', return_value=[mock_attendance]):
                attendances = attendance_service.get_events_by_participant(1)
                assert len(attendances) == 1