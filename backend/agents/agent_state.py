from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from models.segment import Segment

class AgentState(TypedDict):
    meeting_id: str
    messages: Annotated[list[BaseMessage], add_messages]
    transcription: list[dict] #List[dict]
    context: list[dict] #[{id, time_start, time_end, Theme}]
    relevant_dialogues: list[dict] #{theme : dict, dialogues : list[dict]} {theme: id, str}
    draft: str
    iteration: int #num_iteration - prevent infinite loops
    segments_to_inquire: list[Segment] #segments to determine each one of the speakers.
    speaker_names: dict #list to save speaker names [key, name] ex: ["SPEAKER_00", "Daniel"]
    output_file: str


