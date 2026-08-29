from agents.base_agent import BaseAgent
from agents.agent_state import AgentState
from models.segment import Segment
from langgraph.types import interrupt

class IdentificationAgent(BaseAgent):
    def reasoning_node(self, agent_state: AgentState):
        '''
        Iterates through each segment of the transcript. It will extract one excert per speaker.
        Each excerpt has start_time, end_time, text, and speaker.
        '''
        
        speakers = []
        segments_to_inquire = []
        transcript = Segment.transcript_to_segments(agent_state.get("transcription"))
        for segment in transcript:
            if segment.speaker not in speakers:
                speakers.append(segment.speaker)
                segments_to_inquire.append(segment)

        return {
            "segments_to_inquire" : segments_to_inquire
        }

        


    def output_node(self, agent_state: AgentState):
        '''
        The output_node will alter the transcript and put the correct speaker name into the transcript.
        '''
        print("We now know the speakers names!")
        print(agent_state.get("speaker_names"))

        return

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