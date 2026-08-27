from abc import ABC, abstractmethod
from agents.agent_state import AgentState

class BaseAgent(ABC):
    @abstractmethod
    def reasoning_node(agent_state: AgentState):
        '''
        Every agent will have a reasoning node. Perform a task, may require llm.
        '''
        pass

    @abstractmethod
    def output_node(agent_state: AgentState):
        '''
        Every agent will have an output node. Return something or alter something.
        '''
        pass