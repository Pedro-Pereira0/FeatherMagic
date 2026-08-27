from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    transcription: str #Type might be wrong JSON?
    context: list[dict] #[time_start, time_end - Theme] [str, str]
    relevant_dialogues: list[dict] #[theme - list[speaker, dialogue]] [str, list[dict]]
    draft: list[dict] #[type of text - text] [str, str]
    iteration: int #num_iteration - prevent infinite loops


