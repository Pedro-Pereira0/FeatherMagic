from agents.agent_state import AgentState
from core._amalia import reason_model_amalia
from core._gemini import reason_model_gemini
from pathlib import Path
import json

PROMPTS_DIR = Path(__file__).parent / "prompts" / "writing_agent"
CONTEXT_AGENT_PROMPT = (PROMPTS_DIR / "WRITING_AGENT.md").read_text(encoding="utf-8")

class WritingAgent:

    def __init__():
        pass

    def generate_draft(self, agent_state: AgentState):
        '''Node that will generate a draft of the meeting report based on the context and relevant dialogues.'''
        pass