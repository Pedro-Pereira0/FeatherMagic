from datetime import date as date_type, time as time_type

from sqlalchemy import Date, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    creator: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    num_of_participants: Mapped[int] = mapped_column(Integer, nullable=False)

    transcription: Mapped[str] = mapped_column(String, nullable = True)

    def get_id(self) -> int:
        return self.id
    
    def get_title(self) -> str:
        return self.title
    
    def get_creator(self) -> str:
        return self.creator
    
    def get_description(self) -> str:
        return self.description
    
    def get_date(self) -> date_type:
        return self.date
    
    def get_num_of_participants(self) -> int:   
        return self.num_of_participants

    def get_transcription(self) -> str:
        return self.transcription

    def set_transcription(self, transcription: str):
        self.transcription = transcription
        