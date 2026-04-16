from typing import List
from .base import AgentState

def clarifier_agent(state: AgentState):
    """
    Detects ambiguity in requirements and generates clarification questions.
    """
    requirements = state.get("requirements", "")
    
    # In a real implementation, call an LLM here:
    # prompt = f"Analyze these requirements and list ambiguities: {requirements}"
    # response = llm.invoke(prompt)
    
    questions = []
    if not requirements or len(requirements) < 50:
        questions.append("The requirements seem too brief. Can you provide more details on the core functionality?")
    
    if "user" not in requirements.lower():
        questions.append("Who are the primary users of this system?")

    if "database" not in requirements.lower():
        questions.append("Are there any specific database preferences (e.g., PostgreSQL, Neo4j)?")

    status = "awaiting_clarification" if questions else "clarified"
    
    return {
        "clarification_questions": questions,
        "status": status
    }
