from pydantic import BaseModel, ConfigDict
from datetime import date


class MeetingView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    creator: str
    description: str
    date: date
    num_of_participants: int
    language: str