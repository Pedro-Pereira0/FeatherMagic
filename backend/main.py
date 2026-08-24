from fastapi import FastAPI
from api.routers.meetingRouter import meeting_router

app = FastAPI()
app.include_router(meeting_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)