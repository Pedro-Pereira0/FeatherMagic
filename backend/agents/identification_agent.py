from agents.base_agent import BaseAgent
from agents.agent_state import AgentState
from models.segment import Segment

class IdentificationAgent(BaseAgent):
    speakers: list[dict] #a list of [str, str] ex: ["SPEAKER_00", "Jonh"]

    def reasoning_node(self, agent_state: AgentState):
        '''
        The identifcation reasoning node will: 
        1. receive the transcript, 
        2. extract the speakers, 
        3. interrupt the graph and ask the user who the speaker is, with an excert of audio (if possible)
        '''
        speakers = []
        transcript = Segment.transcript_to_segments(agent_state.get("transcription"))
        for segment in transcript:
            if segment.speaker not in speakers:
                speakers.append(segment.speaker)

        print(speakers)


    def output_node(self, agent_state: AgentState):
        '''
        The output_node will alter the transcript and put the correct speaker name into the transcript.
        '''
        pass