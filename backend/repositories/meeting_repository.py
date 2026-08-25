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
        

    def search(self, query):
        # Implement search logic based on the query
        pass