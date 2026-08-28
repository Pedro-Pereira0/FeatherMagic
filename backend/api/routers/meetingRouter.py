from fastapi import APIRouter, File, UploadFile
from api.requests.createMeetingRequest import createMeetingRequest
from api.services.meetingService import MeetingService
from api.views.meeting_view import MeetingView
from api.views.meeting_update_view import MeetingUpdateView

meeting_router = APIRouter()
meeting_service = MeetingService()

@meeting_router.put("/meeting/")
async def create_meeting(meeting_request: createMeetingRequest):
    new_meeting = meeting_service.create_meeting(meeting_request)
    return {"message": "Meeting created successfully", "meeting": MeetingView.model_validate(new_meeting)}

@meeting_router.put("/meeting/{meeting_id}/audio")
async def upload_audio(meeting_id: int, audio_file: UploadFile = File(...)):
    updated_meeting = meeting_service.upload_audio(meeting_id, audio_file)
    return {"message": f"Audio file uploaded for meeting {meeting_id}:", "meeting": MeetingUpdateView.model_validate(updated_meeting)}

@meeting_router.get("/meeting/{meeting_id}/start")
async def start_write_report(meeting_id: int):
    #The report may return incomplete. For example, at the stage of speaker identification.
    #Todo: Need to keep in mind.
    result = meeting_service.start_report_writing(meeting_id)
    return {"message": f"Report generated"}