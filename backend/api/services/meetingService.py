#todo fazer serviços
from api.requests.createMeetingRequest import createMeetingRequest
from repositories.meeting_repository import MeetingRepository
from models.meeting import Meeting

meeting_repo = MeetingRepository()

class MeetingService:
    def __init__(self):
        pass

    def create_meeting(self, meeting_request: createMeetingRequest):
        new_meeting = Meeting(
            title=meeting_request.title,
            creator=meeting_request.creator,
            description=meeting_request.description,
            date=meeting_request.date,
            num_of_participants=meeting_request.num_of_participants
        )

        new_meeting = meeting_repo.create(new_meeting)
        return new_meeting