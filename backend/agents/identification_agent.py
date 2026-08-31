from agents.agent_state import AgentState
from models.segment import Segment
from langgraph.types import interrupt

class IdentificationAgent:
    def extract_speaker_id(self, agent_state: AgentState):
        '''
        Iterates through each segment of the transcript. It will extract one excert per speaker.
        Each excerpt has start_time, end_time, text, and speaker.
        '''
        
        speakers = []
        segments_to_inquire = []
        segments = Segment.transcript_to_segments(agent_state.get("transcription"))
        for segment in segments:
            if segment.speaker not in speakers:
                speakers.append(segment.speaker)
                segments_to_inquire.append(segment)

        return {
            "segments_to_inquire" : segments_to_inquire
        }

    def apply_speaker_name(self, agent_state: AgentState):
        '''
        The output_node will alter the transcript and put the correct speaker name into the transcript.
        '''
        speakers = agent_state.get("speaker_names")
        transcript = agent_state.get("transcription")

        segments = Segment.transcript_to_segments(agent_state.get("transcription"))

        #Alter the transcript to the correct names
        for segment in segments:
            segment.speaker = speakers.get(segment.speaker)

        transcript = Segment.segments_to_transcript(segments)
        return {
            "transcription" : transcript
        }

    def inquire_user(self, agent_state: AgentState):
        segments_to_inquire = agent_state.get("segments_to_inquire")
        speaker_names = agent_state.get("speaker_names")

        if segments_to_inquire:
            segment = segments_to_inquire[-1]

            speaker_name = interrupt({
                "speaker": segment.speaker,
                "text": segment.text,
                "start": segment.start,
                "end": segment.end,
            })

            segments_to_inquire.pop()
            speaker_names[segment.speaker] = speaker_name

        return{
            "segments_to_inquire": segments_to_inquire,
            "speaker_names": speaker_names
        }