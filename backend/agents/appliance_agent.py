from pathlib import Path
from agents.tools import TOOLS
from docx import Document
import os
from langchain_core.messages import HumanMessage, SystemMessage
from agents.agent_state import AgentState

from core._gemini import reason_model_gemini

PROMPTS_DIR = Path(__file__).parent / "prompts" / "appliance_agent"
APPLIANCE_PROMPT = (PROMPTS_DIR / "APPLIANCE_AGENT_PROMPT.md").read_text(encoding="utf-8")

class ApplianceAgent:
    def __init__(self):
        self.model_with_tools = reason_model_gemini.bind_tools(TOOLS)

    def appliance_in_docx(self, agent_state: AgentState):
        '''
        Will use tool calls to apply the draft to a docx file.
        '''
        file_name = agent_state.get("meeting_id") + ".docx"
        path = os.getenv("DOCX_STORAGE_PATH") + "/" + file_name
        if not os.path.exists(path):
            doc = Document()
            doc.save(path)
        
        message = [
            SystemMessage(content=APPLIANCE_PROMPT),
            HumanMessage(content=agent_state.get("draft", "")),
            HumanMessage(content=file_name),
            *agent_state.get("messages", []),
        ]

        response = self.model_with_tools.invoke(message)

        return{
            "messages":[response],
            "iteration": agent_state.get("iteration", 0) + 1
        }

    def appliance_output(self, agent_state: AgentState):
        '''
        Node that will output the final result of the workflow.
        '''
        file_name = agent_state.get("meeting_id") + ".docx"
        path = os.getenv("DOCX_STORAGE_PATH") + "/" + file_name
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {file_name} not found in {os.getenv('DOCX_STORAGE_PATH')}")
        
        return {
            "output_file": path
        }

    
