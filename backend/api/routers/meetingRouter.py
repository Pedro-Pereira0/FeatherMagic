from fastapi import APIRouter
from api.requests.createMeetingRequest import createMeetingRequest
from api.services.meetingService import MeetingService
from api.views.meeting_view import MeetingView

meeting_router = APIRouter()
meeting_service = MeetingService()

@meeting_router.put("/meeting/")
async def create_meeting(meeting_request: createMeetingRequest):
    new_meeting = meeting_service.create_meeting(meeting_request)
    return {"message": "Meeting created successfully", "meeting": MeetingView.model_validate(new_meeting)}