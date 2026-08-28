from fastapi import UploadFile
from api.requests.createMeetingRequest import createMeetingRequest
from repositories.meeting_repository import MeetingRepository
from models.meeting import Meeting
from core.whisperX import WhisperX
import shutil
from utils.utils import Utils
from models.segment import Segment
from agents.state_graph import AgentWorkflow
import json

AUDIO_STORAGE_PATH = "backend/temp/audios"

meeting_repo = MeetingRepository()
#inesc-id/WhisperLv3-EP-X
#inesc-id/WhisperLv3-X-PT-All

my_whisperx = WhisperX(batch_size = 4)
class MeetingService:

    def create_meeting(self, meeting_request: createMeetingRequest):
        new_meeting = Meeting(
            title=meeting_request.title,
            creator=meeting_request.creator,
            description=meeting_request.description,
            date=meeting_request.date,
            num_of_participants=meeting_request.num_of_participants
        )

        new_meeting = meeting_repo.create(new_meeting)

        return new_meeting

    def upload_audio(self, meeting_id: int, audio_file : UploadFile):
        shutil.copyfileobj(audio_file.file, open(f"{AUDIO_STORAGE_PATH}/meeting_{meeting_id}.mp3", "wb"))
        audio_file_path = f"{AUDIO_STORAGE_PATH}/meeting_{meeting_id}.mp3"

        meeting = meeting_repo.get_by_id(meeting_id)

        audio, result = my_whisperx.transcribe(audio_file_path)
        result_aligned = my_whisperx.align(audio, result)
        result_diarized = my_whisperx.diarization(audio,result_aligned, meeting.get_num_of_participants())

        Utils.output_text(result_diarized)        

        meeting.set_transcription(json.loads(json.dumps(result_diarized["segments"], default = "str")))
        
        return meeting_repo.update(meeting)

    def start_report_writing(self, meeting_id: int):
        meeting = meeting_repo.get_by_id(meeting_id)
        if meeting.get_transcription() == None:
            print("No transcription") #Exception
            return

        print("Start the writing of the report")

        initial_state = {
            "messages": [],
            "transcription": meeting.get_transcription(),
            "context": [], 
            "relevant_dialogues": [],
            "draft": [], 
            "iteration": 0, 
        }

        graph = AgentWorkflow().build_graph()
        graph.invoke(initial_state)
        
        return 

    def continue_report_writing(self, meeting_id: int, thread_id: str):
        pass