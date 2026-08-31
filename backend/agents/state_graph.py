from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.agent_state import AgentState

from agents.identification_agent import IdentificationAgent
from agents.context_agent import ContextAgent
from agents.writing_agent import WritingAgent
from agents.appliance_agent import ApplianceAgent

class AgentWorkflow:

    def __init__(self):
        self.id_agent = IdentificationAgent()
        self.context_agent = ContextAgent()

    def identification_condition(self, agent_state: AgentState):
        if agent_state.get("segments_to_inquire"):
            return "id_inquiring"
        else:
            return "id_apply_speaker_name"


    def build_graph(self, checkpointer = None):
        builder = StateGraph(AgentState)

        #Identification
        builder.add_node("id_extract_speaker_id", self.id_agent.extract_speaker_id)
        builder.add_node("id_inquiring", self.id_agent.inquire_user)
        builder.add_node("id_apply_speaker_name", self.id_agent.apply_speaker_name)

        #Context
        builder.add_node("context_id_theme", self.context_agent.identify_theme)
        builder.add_node("context_relevant_dialog_per_theme", self.context_agent.relevant_dialog_per_theme)

        builder.add_edge(START, "id_extract_speaker_id")
        builder.add_conditional_edges("id_extract_speaker_id", 
                                      self.identification_condition, 
                                      ["id_inquiring", "id_apply_speaker_name"])
        
        builder.add_conditional_edges("id_inquiring", 
                                      self.identification_condition,
                                      ["id_inquiring", "id_apply_speaker_name"])

        builder.add_edge("id_apply_speaker_name", "context_id_theme")
        builder.add_edge("context_id_theme", "context_relevant_dialog_per_theme")
        builder.add_edge("context_relevant_dialog_per_theme", END)

        return builder.compile(checkpointer=checkpointer)