from fastapi import APIRouter, File, UploadFile
from api.requests.continue_report_gen_request import ContinueReportGenRequest
from api.requests.create_meeting_request import CreateMeetingRequest
from api.services.meeting_service import MeetingService
from api.views.meeting_view import MeetingView
from api.views.meeting_update_view import MeetingUpdateView
from utils.utils import Utils
import base64
import os

meeting_router = APIRouter()
meeting_service = MeetingService()

@meeting_router.put("/meeting/")
async def create_meeting(meeting_request: CreateMeetingRequest):
    '''
    Args: meeting_request : CreateMeetingRequest
    Returns: Json {message, meetingView}

    This method receives a request to create a new meeting.
    '''
    
    new_meeting = meeting_service.create_meeting(meeting_request)
    return {
        "message": "Meeting created successfully", 
        "meeting": MeetingView.model_validate(new_meeting)
    }

@meeting_router.put("/meeting/{meeting_id}/audio")
async def upload_audio(meeting_id: int, audio_file: UploadFile = File(...)):
    '''
    Args: meeting_id : int, audio_file : UploadFile
    Return: json {message, meetingUpdateView}

    This method receives an audio file, transcribes it and updates a meeting object with it.
    Returns the updated meeting (includign the transcript)
    '''

    updated_meeting = meeting_service.upload_audio(meeting_id, audio_file)
    return {
        "message": f"Audio file uploaded for meeting {meeting_id}:", 
        "meeting": MeetingUpdateView.model_validate(updated_meeting)
    }

@meeting_router.get("/meeting/{meeting_id}/start")
async def start_write_report(meeting_id: int):
    '''
    Args: meeting_id : int
    Returns: json {message, question(if the graph is interrupted with a question to the user "default"), audio_base64, audio_format}

    This method starts the process of creating the report. Returns a question and audio if the question is about the speakers identity.
    '''

    audio_file_path = f"{os.getenv("AUDIO_STORAGE_PATH")}/meeting_{meeting_id}.mp3"
    result = meeting_service.start_report_writing(meeting_id)
    if result.get("__interrupt__"):
        interrupt_obj = result["__interrupt__"][0]
        speaker_id_info = interrupt_obj.value

        audio_bytes = Utils.extract_dialogue(audio_file_path, speaker_id_info.get("start"), speaker_id_info.get("end"))
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "message": f"Report paused.",
            "question": speaker_id_info,
            "audio_base64": audio_b64,
            "audio_format": "wav"
        }
    else:
        return {
            "message": f"Report generated successfully"
        }

@meeting_router.get("/meeting/{meeting_id}/continue")
async def continue_write_report(meeting_id: int, continueReportGenRequest: ContinueReportGenRequest):
    '''
    Args: meeting_id : int, continueReportGenRequest : ContinueReportGenRequest
    Returns: json {message, question(if the graph is interrupted with a question to the user "default"), audio_base64, audio_format}

    This method resumes a previous report generation. It sends the user input under a DTO ContinueReportGenRequest.
    it returns a question and audio if the question is about the speakers identity or only a message if the report is generated.
    '''
  
    user_input = continueReportGenRequest.user_input
    print(user_input)
    audio_file_path = f"{os.getenv("AUDIO_STORAGE_PATH")}/meeting_{meeting_id}.mp3"
    result = meeting_service.continue_report_writing(meeting_id, user_input)

    if result.get("__interrupt__"):
        interrupt_obj = result["__interrupt__"][0]
        speaker_id_info = interrupt_obj.value

        audio_bytes = Utils.extract_dialogue(audio_file_path, speaker_id_info.get("start"), speaker_id_info.get("end"))
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "message": f"Report paused.",
            "question": speaker_id_info,
            "audio_base64": audio_b64,
            "audio_format": "wav"
        }
    else:
        return {
            "message": f"Report generated successfully"
        }