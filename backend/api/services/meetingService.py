#todo fazer serviços
from fastapi import UploadFile
from api.requests.createMeetingRequest import createMeetingRequest
from repositories.meeting_repository import MeetingRepository
from models.meeting import Meeting
from models.whisperX import WhisperX
import shutil
from utils.utils import Utils

AUDIO_STORAGE_PATH = "backend/temp/audios"

meeting_repo = MeetingRepository()
#inesc-id/WhisperLv3-EP-X - X
#inesc-id/WhisperLv3-X-PT-All - X
#

my_whisperx = WhisperX(model_name = "large-v3", batch_size = 4, language = "pt")
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
        #Implement pipeline of audio ingestion and transcription, and then save the transcription to the database
        # 1. Transcribe each audio using WhisperX
        # 2. Align the transcription with the audio
        # 3. Diarization of the audio, to identify speakers and their respective segments
        # 4. Save the transcription

        audio, result = my_whisperx.transcribe(audio_file_path)
        result_aligned = my_whisperx.align(audio, result)
        result_diarized = my_whisperx.diarization(audio, result_aligned, 3)

        Utils.output_text(result_diarized)

        pass