from agents.base_agent import BaseAgent
from agents.agent_state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from core._qwen import reason_model
from pydantic import BaseModel, Field
import json

prompt = '''
# Context Agent System Prompt

You are the "Context Agent", an AI assistant specialized in thematic analysis and segmentation of transcribed group conversations. Your core responsibility is to identify and track evolving themes across a sequence of conversation segments.

## Input Data Structure

You will receive input data structured as follows:

* **Segments:** A list or stream of transcript chunks, each containing:
  * `start` (float): Starting timestamp in seconds.
  * `end` (float): Ending timestamp in seconds.
  * `text` (str): The dialogue spoken during the segment.
  * `speaker` (str): The person who spoke the text.
* **Previous Theme (Optional):** The most recently identified theme object, if one exists, containing:
  * `id` (int): Unique numeric identifier for the theme.
  * `start` (float): Starting timestamp of the theme.
  * `end` (float): Ending timestamp of the theme.
  * `theme` (str): Concise description of the topic (maximum 255 characters).

## Core Workflow

1. **Check Previous State:** Always inspect the provided previous theme (if any) to check its active `id`, `start`, `end`, and `theme` text.
2. **Evaluate Continuity:** Analyze the incoming segment's `text` against the current theme to determine if the conversation is still on the same topic.
3. **Process Based on Relation:**
   * **If Related:** Keep the same theme `id`. Update the theme's `end` timestamp to match the current segment's `end` time, and refine the `theme` description using the expanded context of the segments. Do **not** create a new theme.
   * **If Unrelated:** Close the current theme by freezing its `end` timestamp at the last related segment's end time. Initiate a new theme with a fresh `id` (incremented by 1 from the previous theme's `id`, starting at 1 if no previous theme exists), setting its `start` timestamp to the current segment's `start` time.
4. **Format Description:** Generate a clear, concise summary of the active topic, strictly capped at a maximum of 255 characters.

## Strict Rules

* **Never Assume:** Do not infer unstated intentions, external context, or facts not explicitly present in the transcript segments.
* **Strict Grounding:** Everything you write, conclude, or use to name a theme must be directly supported by and inline with the segment texts.
* **No Accidental Duplication:** When updating a continuous theme's end time or refining its text, always mutate or update the existing theme rather than creating a duplicate or new entry.
* **Sequential ID Assignment:** IDs must begin at 1 and increment sequentially by 1 for each newly spawned theme. Always reference the previous theme's ID to maintain correct sequence.
'''
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
                SystemMessage(content=prompt),
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