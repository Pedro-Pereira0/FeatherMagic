from agents.agent_state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage
from core._amalia import writer_model_amalia
from core._gemini import reason_model_gemini
from core._groq import reason_model_groq
from core._qwen import reason_model_qwen
from agents.base_agent import base_agent
from pathlib import Path
import json

PROMPTS_DIR = Path(__file__).parent / "prompts" / "writing_agent"
WRITING_AGENT_PROMPT = (PROMPTS_DIR / "WRITING_AGENT.md").read_text(encoding="utf-8")

class WritingAgent(base_agent):
    def __init__(self, language: str):
        #Using the same model, for now
        if language == "pt":
            self.writing_agent = reason_model_groq
        else:
            self.writing_agent = reason_model_groq

    def generate_draft(self, agent_state: AgentState):
        '''Node that will generate a draft of the meeting report based on the context and relevant dialogues.'''
        print("Writing Agent: generating draft")
        relevant_dialogues = agent_state.get("relevant_dialogues")
        message = [
            SystemMessage(content = WRITING_AGENT_PROMPT),
            HumanMessage(content=json.dumps(relevant_dialogues))
        ]

        response = self.writing_agent.invoke(self.sanitize_messages(message))
        if response and response.content:
            print(response.content)
        return {
            "draft": response.content
        }