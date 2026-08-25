#todo fazer serviços
from fastapi import UploadFile
from api.requests.createMeetingRequest import createMeetingRequest
from repositories.meeting_repository import MeetingRepository
from models.meeting import Meeting
from models.whisperX import WhisperX
import shutil
from pathlib import Path

AUDIO_STORAGE_PATH = "backend/temp/audios"
OUTPUT_STORAGE_PATH = "backend/temp/outputs"

meeting_repo = MeetingRepository()
#inesc-id/WhisperLv3-EP-X - X
#inesc-id/WhisperLv3-X-PT-All - X
#

my_whisperx = WhisperX(model_name = "inesc-id/WhisperLv3-EP-X", batch_size = 4, language="pt")
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
         #UploadFile(filename='reuniao_1.mp3', size=2025529, headers=Headers({'content-disposition': 'form-data; name="audio_file"; filename="reuniao_1.mp3"', 'content-type': 'audio/mpeg'}))
        shutil.copyfileobj(audio_file.file, open(f"{AUDIO_STORAGE_PATH}/meeting_{meeting_id}.mp3", "wb"))
        audio_file_path = f"{AUDIO_STORAGE_PATH}/meeting_{meeting_id}.mp3"
        #Implement pipeline of audio ingestion and transcription, and then save the transcription to the database
        # 1. Transcribe each audio using WhisperX
        # 2. Align the transcription with the audio
        # 3. Diarization of the audio, to identify speakers and their respective segments
        # 4. Save the transcription

        audio, result = my_whisperx.transcribe(audio_file_path)
        result_aligned = my_whisperx.align(audio, result)
        result_diarized = my_whisperx.diarization(audio, result_aligned, 3, 2, 3)
        print(result_diarized["segments"])
        self.output_text(result_diarized)

        pass

    def output_text(self, results):
        output_directory = Path(OUTPUT_STORAGE_PATH)
        output_directory.mkdir(parents=True, exist_ok=True)

        output_file_path = output_directory / "output.txt"
        readable_segments = []
        for segment in results.get("segments", []):
            start = segment.get("start", 0)
            end = segment.get("end", 0)
            speaker = segment.get("speaker", "UNKNOWN")
            text = segment.get("text", "").strip()

            readable_segments.append(
                f"[{self._format_timestamp(start)} - {self._format_timestamp(end)}] "
                f"{speaker}: {text}"
            )

        output_file_path.write_text("\n\n".join(readable_segments), encoding="utf-8")

        return str(output_file_path)

    @staticmethod
    def _format_timestamp(seconds):
        total_seconds = int(float(seconds))
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
