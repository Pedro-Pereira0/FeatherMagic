from pydantic import BaseModel

class createMeetingRequest(BaseModel):
    title: str
    creator: str
    description: str
    date: str
    start_time: str
    end_time: str
    num_of_participants: int
