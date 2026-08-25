#todo fazer serviços
from api.requests.createMeetingRequest import createMeetingRequest
from models.meeting import Meeting

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
        #todo: save new_meeting to the repository
        return new_meeting