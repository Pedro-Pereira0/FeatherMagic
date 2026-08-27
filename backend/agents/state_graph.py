from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.agent_state import AgentState
from langgraph.checkpoint.sqlite import SqliteSaver

from agents.identification_agent import IdentificationAgent
from agents.context_agent import ContextAgent
from agents.writing_agent import WritingAgent
from agents.appliance_agent import ApplianceAgent

class AgentWorkflow:

    def build_graph(db_path: str = "checkpoints.sqlite"):
        builder = StateGraph(AgentState)

        checkpointer = SqliteSaver.from_conn_string(db_path)
        return builder.compile(checkpointer = checkpointer)
