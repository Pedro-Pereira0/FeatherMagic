from pydantic import BaseModel
from datetime import date, time

class createMeetingRequest(BaseModel):
    title: str
    creator: str
    description: str
    date: date
    num_of_participants: int
