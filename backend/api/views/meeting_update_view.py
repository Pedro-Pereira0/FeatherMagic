
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Any
class MeetingUpdateView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    num_of_participants: int
    transcription: Any