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
            return "id_output"


    def build_graph(self, checkpointer = None):
        builder = StateGraph(AgentState)

        #Identification
        builder.add_node("id_reasoning", self.id_agent.reasoning_node)
        builder.add_node("id_inquiring", self.id_agent.inquire_user)
        builder.add_node("id_output", self.id_agent.output_node)

        #Context
        builder.add_node("context_reasoning", self.context_agent.reasoning_node)
        builder.add_node("context_output", self.context_agent.output_node)

        builder.add_edge(START, "id_reasoning")
        builder.add_conditional_edges("id_reasoning", 
                                      self.identification_condition, 
                                      ["id_inquiring", "id_output"])
        
        builder.add_conditional_edges("id_inquiring", 
                                      self.identification_condition,
                                      ["id_inquiring", "id_output"])

        builder.add_edge("id_output", END)

        return builder.compile(checkpointer=checkpointer)