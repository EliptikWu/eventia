from events.repositories.attendance_repository import AttendanceRepository
from events.repositories.event_repository import EventRepository
from events.repositories.participant_repository import ParticipantRepository


class AttendanceService:
    def __init__(self):
        self.attendance_repository = AttendanceRepository()
        self.event_repository = EventRepository()
        self.participant_repository = ParticipantRepository()

    def register_attendance(self, event_id, participant_id):
        # Validar que el evento existe
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found")

        # Validar que el participante existe
        participant = self.participant_repository.get_by_id(participant_id)
        if participant is None:
            raise ValueError("Participant not found")

        # Validar que no esté registrado
        existing = self.attendance_repository.get_by_event_and_participant(event_id, participant_id)
        if existing:
            raise ValueError("Participant is already registered for this event")

        # Validar capacidad
        current_attendees = self.attendance_repository.count_by_event(event_id)
        if current_attendees >= event.max_capacity:
            raise ValueError("Event is at full capacity")

        # Registrar asistencia
        return self.attendance_repository.create(event_id, participant_id)

    def cancel_attendance(self, event_id, participant_id):
        success = self.attendance_repository.delete(event_id, participant_id)
        if not success:
            raise ValueError("Attendance record not found")
        return success

    def get_attendees_by_event(self, event_id):
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found")
        return self.attendance_repository.get_by_event(event_id)

    def get_events_by_participant(self, participant_id):
        participant = self.participant_repository.get_by_id(participant_id)
        if participant is None:
            raise ValueError("Participant not found")
        return self.attendance_repository.get_by_participant(participant_id)