from agents.base_agent import BaseAgent
from agents.agent_state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from core._qwen import reason_model
from pydantic import BaseModel, Field
from agents.prompts.prompts import CONTEXT_AGENT_PROMPT
import json

class _Theme(BaseModel):
    id: int
    start: float
    end: float
    theme: str = Field(max_length=255)

class _ThemeList(BaseModel):
    theme_list : list[_Theme]

class ContextAgent(BaseAgent):

    def __init__(self):
        self.struct_model = reason_model.with_structured_output(_ThemeList)

    def reasoning_node(self, agent_state: AgentState):
        '''
        The context agent will read the script and define the main themes in discussion during the meeting.
        It will use the timestamps of the text to deterimine the timestamp of the theme. It will also extract the most relevant
        phrases and its speaker.
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
        print(no_duplicate_themes)
        pass

    def output_node(self, agent_state: AgentState):
        pass


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