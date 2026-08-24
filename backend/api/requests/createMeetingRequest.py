from pydantic import BaseModel
from datetime import date, time

class createMeetingRequest(BaseModel):
    title: str
    creator: str
    description: str
    date: date
    duration: time
    num_of_participants: int
