from fastapi import APIRouter, File, UploadFile
import shutil
from api.requests.createMeetingRequest import createMeetingRequest
from api.services.meetingService import MeetingService
from api.views.meeting_view import MeetingView

meeting_router = APIRouter()
meeting_service = MeetingService()

AUDIO_STORAGE_PATH = "backend/temp"

@meeting_router.put("/meeting/")
async def create_meeting(meeting_request: createMeetingRequest):
    new_meeting = meeting_service.create_meeting(meeting_request)
    return {"message": "Meeting created successfully", "meeting": MeetingView.model_validate(new_meeting)}

@meeting_router.put("/meeting/{meeting_id}/audio")
async def upload_audio(meeting_id: int, audio_file: UploadFile = File(...)):
    #UploadFile(filename='reuniao_1.mp3', size=2025529, headers=Headers({'content-disposition': 'form-data; name="audio_file"; filename="reuniao_1.mp3"', 'content-type': 'audio/mpeg'}))
    shutil.copyfileobj(audio_file.file, open(f"{AUDIO_STORAGE_PATH}/meeting_{meeting_id}.mp3", "wb"))
    return {"message": f"Audio file uploaded for meeting {meeting_id}"}