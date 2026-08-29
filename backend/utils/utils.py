from pathlib import Path
from pydub import AudioSegment
import io

OUTPUT_STORAGE_PATH = "backend/temp/outputs"

class Utils:
    @staticmethod
    def output_text(results):
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
                f"[{Utils._format_timestamp(start)} - {Utils._format_timestamp(end)}] "
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

    @staticmethod
    def extract_dialogue(path:str, start:float, end:float):
        audio = AudioSegment.from_file(path)
        clip = audio[int(start * 1000):int(end * 1000)]
        
        buffer = io.BytesIO()
        clip.export(buffer, format="wav")
        return buffer.getvalue()
