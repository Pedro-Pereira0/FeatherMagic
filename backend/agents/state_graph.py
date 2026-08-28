from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.agent_state import AgentState
from langgraph.checkpoint.sqlite import SqliteSaver

from agents.identification_agent import IdentificationAgent
from agents.context_agent import ContextAgent
from agents.writing_agent import WritingAgent
from agents.appliance_agent import ApplianceAgent

class AgentWorkflow:

    def __init__(self):
        self.id_agent = IdentificationAgent()

    def build_graph(self, db_path: str = "checkpoints.sqlite"):
        builder = StateGraph(AgentState)

        builder.add_node("id_reasoning", self.id_agent.reasoning_node)

        builder.add_edge(START, "id_reasoning")
        builder.add_edge("id_reasoning", END)

        #checkpointer = SqliteSaver.from_conn_string(db_path)
        #return builder.compile(checkpointer = checkpointer)
        return builder.compile()
