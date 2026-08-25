from fastapi import APIRouter, File, UploadFile
from api.requests.createMeetingRequest import createMeetingRequest
from api.services.meetingService import MeetingService
from api.views.meeting_view import MeetingView

meeting_router = APIRouter()
meeting_service = MeetingService()

@meeting_router.put("/meeting/")
async def create_meeting(meeting_request: createMeetingRequest):
    new_meeting = meeting_service.create_meeting(meeting_request)
    return {"message": "Meeting created successfully", "meeting": MeetingView.model_validate(new_meeting)}

@meeting_router.put("/meeting/{meeting_id}/audio")
async def upload_audio(meeting_id: int, audio_file: UploadFile = File(...)):
    meeting_service.upload_audio(meeting_id, audio_file)
    return {"message": f"Audio file uploaded for meeting {meeting_id}"}