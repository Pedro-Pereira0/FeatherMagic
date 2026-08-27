import whisperx
from whisperx.diarize import DiarizationPipeline, Pipeline
import os
from utils.utils import Utils

class WhisperX:
    device: str
    batch_size: int
    compute_type: str
    model_name: str
    language: str
    MODEL_PATH = "backend/temp/models/"

    def __init__(self, device = "cuda", batch_size: int = 16, compute_type: str = "float16", model_name: str = "large-v3", language: str = "pt"):
        self.device = device
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.model_name = model_name
        self.language = language

    def transcribe(self, audio_file_path: str):
        model = whisperx.load_model(self.model_name, self.device, compute_type = self.compute_type, download_root = self.MODEL_PATH)

        audio = whisperx.load_audio(audio_file_path)
        result = model.transcribe(audio, batch_size=self.batch_size)

        #Remove the model from memory to free up GPU resources
        import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del model
        
        return audio, result

    def align(self, audio, result) -> str:
        align_model, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
        result_aligned = whisperx.align(result["segments"], align_model, metadata, audio, self.device, return_char_alignments=False)

        #Remove the model from memory to free up GPU resources
        import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del align_model

        return result_aligned

    def diarization(self, audio, result_aligned, num_speakers):
        diarize_model = DiarizationPipeline(model_name = "pyannote/speaker-diarization-community-1", token = os.getenv("HUGGING_FACE_TOKEN"), device = self.device)
        
        diarize_segments = diarize_model(audio, num_speakers = num_speakers)

        result_diarized = whisperx.assign_word_speakers(diarize_segments, result_aligned, fill_nearest=True)

        import gc; import torch; gc.collect(); torch.cuda.empty_cache(); del diarize_model

        return result_diarized
