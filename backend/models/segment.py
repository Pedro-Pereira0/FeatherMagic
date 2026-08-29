from pydantic import BaseModel, ConfigDict

class Segment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    start: float
    end: float
    text: str
    speaker: str

    @staticmethod
    def transcript_to_segments(transcript : list[dict]):
        '''
        Args: transcript list[dict], each dict representing a segment
        Returns: a list of segment objects

        Transforms a list of dict to a list of segments of the class Segment. Easy to iterate, view and alter.
        '''
        segment_list = []
        for segment in transcript:
            segment_list.append(Segment.model_validate(segment))

        return segment_list

    @staticmethod
    def segments_to_transcript (segments: list["Segment"]):
        '''
        Args: List of Segments
        Returns: List[dict]

        Transforms a list of segments into a transcript of the type list[dict].
        '''
        return [
            segment.model_dump()
            for segment in segments
        ]
