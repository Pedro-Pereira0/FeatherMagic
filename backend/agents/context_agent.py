from agents.agent_state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from core._gemini import reason_model_gemini
from pydantic import BaseModel, Field
from models.segment import Segment
from pathlib import Path
import json

PROMPTS_DIR = Path(__file__).parent / "prompts" / "context_agent"
CONTEXT_AGENT_PROMPT = (PROMPTS_DIR / "CONTEXT_AGENT_THEME.md").read_text(encoding="utf-8")
CONTEXT_AGENT_PROMPT_DIALOG_EXTRACTION = (
    PROMPTS_DIR / "CONTEXT_AGENT_DIALOG_EXTRACT.md"
).read_text(encoding="utf-8")

class _Theme(BaseModel):
    id: int
    start: float
    end: float
    theme: str = Field(max_length=255)

class _ThemeList(BaseModel):
    theme_list : list[_Theme]

class _Dialog(BaseModel):
    theme_id: int
    start: float
    end: float
    text: str
    speaker: str

class _DialogList(BaseModel):
    dialog_list : list[_Dialog]

class ContextAgent:

    def __init__(self):
        self.struct_model = reason_model_gemini.with_structured_output(_ThemeList)
        self.struct_model_dialog = reason_model_gemini.with_structured_output(_DialogList)

    def identify_theme(self, agent_state: AgentState):
        '''
        The context agent will read the script and define the themes in discussion during the meeting.
        It will use the timestamps of the text to deterimine the timestamp of the theme.
        '''
        transcript = agent_state.get("transcription")
        batch_size = 5
        all_themes = []
        
        # Process transcript in batches of 5 segments
        for i in range(0, len(transcript), batch_size):
            batch = transcript[i:i + batch_size]
            # Convert theme objects to dicts for JSON serialization
            themes_as_dicts = [theme.model_dump() for theme in all_themes]
            messages = [
                SystemMessage(content=CONTEXT_AGENT_PROMPT),
                HumanMessage(content=json.dumps(batch)),
            ]
            if themes_as_dicts:
                messages.append(HumanMessage(content=json.dumps(themes_as_dicts[-1])))
                
            response = self.struct_model.invoke(messages)
            if response and response.theme_list:
                all_themes.extend(response.theme_list)

        no_duplicate_themes = self.remove_duplicates(all_themes)

        context = [theme.model_dump() for theme in no_duplicate_themes]
        
        return {
            "context" : context
        }

    def relevant_dialog_per_theme(self, agent_state: AgentState):
        '''
        This node will extract the most relevant dialogues and their speakers for each theme.
        '''
        themes = agent_state.get("context")
        all_dialogs = []
        segments = Segment.transcript_to_segments(agent_state.get("transcription"))
        for theme in themes:
            segments_batch = []
            for segment in segments:
                if segment.start >= theme.get("start") and segment.end <= theme.get("end"):
                    segments_batch.append(segment)
                elif segment.start > theme.get("end"):
                    break

            #Removes the segments that have already been processed from the list.
            for segment in segments_batch:
                segments.remove(segment)

            batch = [segment_batch.model_dump() for segment_batch in segments_batch]
            messages = [
                SystemMessage(content=CONTEXT_AGENT_PROMPT_DIALOG_EXTRACTION),
                HumanMessage(content="Theme:"+ json.dumps(theme)),
                HumanMessage(content="Segments: " + json.dumps(batch)),
            ]
            response = self.struct_model_dialog.invoke(messages)
            if response and response.dialog_list:
                all_dialogs.extend(response.dialog_list)

        print(all_dialogs)


    def remove_duplicates(self, all_themes: _ThemeList):
        '''
        Args: all_themes
        Returns list[_themes]

        Removes duplicates by removing the first instance (only works if the duplicates are next to each other which is the most common case)
        This behaviour happens because sending and appending potencial themes that have not ended yet.
        '''

        no_duplicates = []
        for theme in all_themes:
            if no_duplicates:
                for new_theme in no_duplicates:
                    if theme.id == new_theme.id:
                        no_duplicates.remove(new_theme)

            no_duplicates.append(theme)

        return no_duplicates