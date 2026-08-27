from fastapi import FastAPI
from api.routers.meetingRouter import meeting_router
from models.base import Base
from models.meeting import Meeting
from models.user import User
from repositories.database import engine
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(meeting_router)

if __name__ == "__main__":
    import uvicorn
    Base.metadata.create_all(engine)
    uvicorn.run(app, host="localhost", port=8000)