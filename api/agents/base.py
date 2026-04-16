from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

# Import the actual agent functions
from .clarifier import clarifier_agent
from .retriever import retriever_agent
from .decomposer import decomposer_agent
from .estimator import estimator_agent
from .validator import validator_agent
from .feedback import feedback_agent

class AgentState(TypedDict):
    project_id: str
    requirements: str
    clarification_questions: List[str]
    tasks: List[Dict[str, Any]]
    estimations: Dict[str, Any]
    validator_feedback: List[str]
    status: str
    thread_id: str

def create_mage_graph():
    workflow = StateGraph(AgentState)
    
    # Define the nodes
    workflow.add_node("clarifier", clarifier_agent)
    workflow.add_node("retriever", retriever_agent)
    workflow.add_node("decomposer", decomposer_agent)
    workflow.add_node("estimator", estimator_agent)
    workflow.add_node("validator", validator_agent)
    workflow.add_node("feedback", feedback_agent)

    # Define the edges/logic
    workflow.set_entry_point("clarifier")
    
    # Simple linear flow for now
    workflow.add_edge("clarifier", "retriever")
    workflow.add_edge("retriever", "decomposer")
    workflow.add_edge("decomposer", "estimator")
    workflow.add_edge("estimator", "validator")
    workflow.add_edge("validator", END)
    
    return workflow.compile()

mage_app = create_mage_graph()
