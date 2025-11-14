from events.repositories.participant_repository import ParticipantRepository


class ParticipantService:
    def __init__(self):
        self.participant_repository = ParticipantRepository()

    def get_all_participants(self):
        return self.participant_repository.get_all()

    def get_participant_by_id(self, participant_id):
        participant = self.participant_repository.get_by_id(participant_id)
        if participant is None:
            raise ValueError("Participant not found")
        return participant

    def create_participant(self, data):
        email = data.get('email')
        if self.participant_repository.get_by_email(email):
            raise ValueError("A participant with this email already exists")
        return self.participant_repository.create(data)

    def update_participant(self, participant_id, data):
        participant = self.participant_repository.update(participant_id, data)
        if participant is None:
            raise ValueError("Participant not found")
        return participant

    def delete_participant(self, participant_id):
        success = self.participant_repository.delete(participant_id)
        if not success:
            raise ValueError("Participant not found")
        return success