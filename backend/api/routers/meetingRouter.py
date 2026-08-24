from fastapi import APIRouter
from api.requests.createMeetingRequest import createMeetingRequest

meeting_router = APIRouter()

@meeting_router.put("/meeting/")
async def create_meeting(meeting: createMeetingRequest):
    # Logic to create a meeting
    return {"message": "Meeting created successfully", "meeting": meeting}