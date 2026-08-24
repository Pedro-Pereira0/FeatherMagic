from fastapi import FastAPI
from api.routers.meetingRouter import meeting_router
from sqlalchemy import create_engine
from models.base import Base
from models.meeting import Meeting
from models.user import User

app = FastAPI()
app.include_router(meeting_router)
engine = create_engine("sqlite:///./test.db", echo=True)

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(engine)
    uvicorn.run(app, host="localhost", port=8000)