from repositories.repository_interface import RepositoryInterface
from models.meeting import Meeting
from sqlalchemy.orm import Session

from repositories.database import engine

class MeetingRepository(RepositoryInterface):
    def create(self, new_meeting : Meeting):
        with Session(engine) as session:
            session.add(new_meeting)
            session.commit()
            session.refresh(new_meeting)

            return new_meeting

    def update(self, meeting : Meeting):
        with Session(engine) as session:
            merged_meeting = session.merge(meeting)
            session.commit()
            session.refresh(merged_meeting)

            return merged_meeting
        
    def get_by_id(self, meeting_id: int):
        with Session(engine) as session:
            meeting = session.query(Meeting).filter(Meeting.id == meeting_id).first()
            return meeting