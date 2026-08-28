from agents.base_agent import BaseAgent
from agents.agent_state import AgentState
from models.segment import Segment

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

        


    def output_node(self, agent_state: AgentState):
        '''
        The output_node will alter the transcript and put the correct speaker name into the transcript.
        '''
        pass