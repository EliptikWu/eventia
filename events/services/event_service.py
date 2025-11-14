from events.repositories.event_repository import EventRepository
from events.repositories.attendance_repository import AttendanceRepository


class EventService:
    def __init__(self):
        self.event_repository = EventRepository()
        self.attendance_repository = AttendanceRepository()

    def get_all_events(self):
        return self.event_repository.get_all()

    def get_event_by_id(self, event_id):
        event = self.event_repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Event not found")
        return event

    def create_event(self, data):
        if data.get('max_capacity', 0) <= 0:
            raise ValueError("Max capacity must be greater than 0")
        return self.event_repository.create(data)

    def update_event(self, event_id, data):
        event = self.event_repository.update(event_id, data)
        if event is None:
            raise ValueError("Event not found")
        return event

    def delete_event(self, event_id):
        success = self.event_repository.delete(event_id)
        if not success:
            raise ValueError("Event not found")
        return success

    def get_event_statistics(self, event_id):
        event = self.get_event_by_id(event_id)
        total_attendees = self.attendance_repository.count_by_event(event_id)
        available_capacity = event.max_capacity - total_attendees
        occupancy_percentage = (total_attendees / event.max_capacity) * 100 if event.max_capacity > 0 else 0

        return {
            'event_id': event_id,
            'event_name': event.name,
            'max_capacity': event.max_capacity,
            'total_attendees': total_attendees,
            'available_capacity': available_capacity,
            'occupancy_percentage': round(occupancy_percentage, 2),
            'is_full': available_capacity == 0
        }