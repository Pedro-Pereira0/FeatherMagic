from agents.agent_state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from core._amalia import writer_model_amalia
from core._gemini import reason_model_gemini
from core._qwen import reason_model_qwen
from pathlib import Path
import json

PROMPTS_DIR = Path(__file__).parent / "prompts" / "writing_agent"
WRITING_AGENT_PROMPT = (PROMPTS_DIR / "WRITING_AGENT.md").read_text(encoding="utf-8")

class WritingAgent:
    def __init__(self, language: str):
        if language == "pt":
            self.writing_agent = writer_model_amalia
        else:
            self.writing_agent = reason_model_qwen

    def generate_draft(self, agent_state: AgentState):
        '''Node that will generate a draft of the meeting report based on the context and relevant dialogues.'''
        relevant_dialogues = agent_state.get("relevant_dialogues")
        message = [
            SystemMessage(content = WRITING_AGENT_PROMPT),
            HumanMessage(content=json.dumps(relevant_dialogues))
        ]

        response = self.writing_agent.invoke(message)
        if response and response.content:
            print(response.content)
        return {
            "draft": response.content
        }