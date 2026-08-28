from pydantic import BaseModel, ConfigDict

class Segment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    start: float
    end: float
    text: str
    speaker: str

    @staticmethod
    def transcript_to_segments(transcript : list[dict]):
        segment_list = []
        for segment in transcript:
            segment_list.append(Segment.model_validate(segment))

        return segment_list