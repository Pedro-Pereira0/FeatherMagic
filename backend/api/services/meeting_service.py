from fastapi import UploadFile
from langgraph.types import Command
from api.requests.create_meeting_request import CreateMeetingRequest
from repositories.meeting_repository import MeetingRepository
from models.meeting import Meeting
from core.whisperX import WhisperX
import shutil
from utils.utils import Utils
from models.segment import Segment
from agents.state_graph import AgentWorkflow
from langgraph.checkpoint.sqlite import SqliteSaver
import json
import os

meeting_repo = MeetingRepository()
#inesc-id/WhisperLv3-EP-X
#inesc-id/WhisperLv3-X-PT-All

my_whisperx = WhisperX(batch_size = 4)
class MeetingService:

    def create_meeting(self, meeting_request: CreateMeetingRequest):
        '''
        Args: meeting_request : CreateMeetingRequest
        Returns: meeting instance : Meeting

        This method creates an object meeting and saves it into the database.
        '''
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
        '''
        Args: meeting_id:int, audio_file: UploadFile
        Returns: meeting instance: Meeting

        This methods updates the meeting object of meeting_id with the transcription of the audio file uploaded.
        It also saves the resulted segments in an output.txt file.
        '''
        shutil.copyfileobj(audio_file.file, open(f"{os.getenv("AUDIO_STORAGE_PATH")}/meeting_{meeting_id}.mp3", "wb"))
        audio_file_path = f"{os.getenv("AUDIO_STORAGE_PATH")}/meeting_{meeting_id}.mp3"

        meeting = meeting_repo.get_by_id(meeting_id)

        audio, result = my_whisperx.transcribe(audio_file_path)
        result_aligned = my_whisperx.align(audio, result)
        result_diarized = my_whisperx.diarization(audio,result_aligned, meeting.get_num_of_participants())

        Utils.output_text(result_diarized)        

        meeting.set_transcription(json.loads(json.dumps(result_diarized["segments"], default = "str")))
        
        return meeting_repo.update(meeting)

    def start_report_writing(self, meeting_id: int):
        '''
        Args: meeting_id : int
        Returns: result of the invocation of the agent workflow.

        This method starts the process of building the report by invocing the agents workflow graph. The process is saved in sqlite .db, under
        a thread_id.
        '''
        meeting = meeting_repo.get_by_id(meeting_id)
        if meeting is None:
            print("Meeting not found")
            return
        if meeting.get_transcription() is None:
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
            "segments_to_inquire" : [],
            "speaker_names" : {} 
        }
        thread_id = meeting.get_title() + "_" + str(meeting.get_id())

        meeting.set_thread_id(thread_id)
        meeting_repo.update(meeting)
        
        config = {"configurable": {"thread_id": thread_id}}
        with SqliteSaver.from_conn_string("checkpoint.db") as checkpointer:
            graph = AgentWorkflow().build_graph(checkpointer)
            result = graph.invoke(initial_state, config = config)

        return result

    def continue_report_writing(self, meeting_id: int, user_input: str):
        '''
        Args: meeting_id : int, user_input : str
        Returns: The results of the invocation of the agents workflow

        This method resumes a previous started report. This method is used when the user answers an HITL agent question.
        '''
        meeting = meeting_repo.get_by_id(meeting_id)
        if meeting is None:
            print("Meeting not found")
            return
        if meeting.get_transcription() is None:
            print("No transcription") #Exception
            return
        elif meeting.get_thread_id() is None:
            print("No report generation started")
            return

        config = {"configurable": {"thread_id": meeting.get_thread_id()}}
        
        with SqliteSaver.from_conn_string("checkpoint.db") as checkpointer:
            graph = AgentWorkflow().build_graph(checkpointer)
            result = graph.invoke(Command(resume=user_input), config = config)

        return result
        
        

        