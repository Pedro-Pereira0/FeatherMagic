from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from models.segment import Segment

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    transcription: list[dict] #List[dict]
    context: list[dict] #[time_start, time_end, Theme] [str, str]
    relevant_dialogues: list[dict] #[theme - list[speaker, dialogue]] [str, list[dict]]
    draft: list[dict] #[type of text - text] [str, str]
    iteration: int #num_iteration - prevent infinite loops

    segments_to_inquire: list[Segment] #segments to determine each one of the speakers.
    speaker_names: dict #list to save speaker names [key, name] ex: ["SPEAKER_00", "Daniel"]


