from pathlib import Path
from pydub import AudioSegment
import io
import os

class Utils:
    @staticmethod
    def output_text(results):
        '''
        Args: results of the transcription pipeline
        Returns: path of the txt file.

        This method will format the segments extracted from the audio into a more readable format and save the
        results in a output.txt file.
        '''
        output_directory = Path(os.getenv("OUTPUT_STORAGE_PATH"))
        output_directory.mkdir(parents=True, exist_ok=True)

        output_file_path = output_directory / "output.txt"
        readable_segments = []
        for segment in results.get("segments", []):
            start = segment.get("start", 0)
            end = segment.get("end", 0)
            speaker = segment.get("speaker", "UNKNOWN")
            text = segment.get("text", "").strip()

            readable_segments.append(
                f"[{Utils._format_timestamp(start)} - {Utils._format_timestamp(end)}] "
                f"{speaker}: {text}"
            )

        output_file_path.write_text("\n\n".join(readable_segments), encoding="utf-8")

        return str(output_file_path)

    @staticmethod
    def _format_timestamp(seconds):
        '''
        Args: float representing seconds
        Returns: a string with the seconds converted to hours:minutes:seconds

        Used in the output_text method.
        '''
        total_seconds = int(float(seconds))
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @staticmethod
    def extract_dialogue(path:str, start:float, end:float):
        '''
        Args: path to the audio file, start of the audio excert, end of the audio excert
        Returns: bytes of the excert of the audio

        Extracts an audio excert. Starting in start seconds and ending in end seconds.
        This method is to be used to extract a dialogue segment to return to the user.
        '''
        audio = AudioSegment.from_file(path)
        clip = audio[int(start * 1000):int(end * 1000)]
        
        buffer = io.BytesIO()
        clip.export(buffer, format="wav")
        return buffer.getvalue()
