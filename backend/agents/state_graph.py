from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.agent_state import AgentState

from agents.identification_agent import IdentificationAgent
from agents.context_agent import ContextAgent
from agents.writing_agent import WritingAgent
from agents.appliance_agent import ApplianceAgent

from agents.tools import TOOLS

class AgentWorkflow:

    def __init__(self, language: str):
        self.id_agent = IdentificationAgent()
        self.context_agent = ContextAgent()
        self.writing_agent = WritingAgent(language)
        self.appliance_agent = ApplianceAgent()

    def identification_condition(self, agent_state: AgentState):
        if agent_state.get("segments_to_inquire"):
            return "id_inquiring"
        else:
            return "id_apply_speaker_name"

    def route_after_results(self, agent_state: AgentState) -> str:
        last = agent_state["messages"][-1]

        if getattr(last, "tool_calls", None):
            return "tools"
        if agent_state.get("iteration", 0) >= 250:
            return END
        # hard safety stop
        return END

    def build_graph(self, checkpointer = None):
        builder = StateGraph(AgentState)

        builder.add_node("tools", ToolNode(TOOLS))

        #Identification
        builder.add_node("id_extract_speaker_id", self.id_agent.extract_speaker_id)
        builder.add_node("id_inquiring", self.id_agent.inquire_user)
        builder.add_node("id_apply_speaker_name", self.id_agent.apply_speaker_name)

        #Context
        builder.add_node("context_id_theme", self.context_agent.identify_theme)
        builder.add_node("context_relevant_dialog_per_theme", self.context_agent.relevant_dialog_per_theme)

        #Writing
        builder.add_node("writing_draft", self.writing_agent.generate_draft)

        #Appliance
        builder.add_node("appliance_docx", self.appliance_agent.appliance_in_docx)
        builder.add_node("appliance_output", self.appliance_agent.appliance_output)

        builder.add_edge(START, "id_extract_speaker_id")
        builder.add_conditional_edges("id_extract_speaker_id", 
                                      self.identification_condition, 
                                      ["id_inquiring", "id_apply_speaker_name"])
        
        builder.add_conditional_edges("id_inquiring", 
                                      self.identification_condition,
                                      ["id_inquiring", "id_apply_speaker_name"])

        builder.add_edge("id_apply_speaker_name", "context_id_theme")
        builder.add_edge("context_id_theme", "context_relevant_dialog_per_theme")
        builder.add_edge("context_relevant_dialog_per_theme", "writing_draft")
        builder.add_edge("writing_draft", "appliance_docx")

        builder.add_conditional_edges("appliance_docx", 
                                      self.route_after_results,
                                      ["tools", END])
        
        builder.add_edge("tools", "appliance_docx")
        
        builder.add_edge("appliance_output", END)

        return builder.compile(checkpointer=checkpointer)