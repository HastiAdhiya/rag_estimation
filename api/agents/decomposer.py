from .base import AgentState

def decomposer_agent(state: AgentState):
    """
    Breaks requirements into hierarchical tasks and subtasks.
    """
    requirements = state.get("requirements", "")
    
    # In a real implementation, use LLM to parse into JSON tasks:
    # prompt = f"Decompose these requirements into a task list: {requirements}"
    
    tasks = [
        {"id": 1, "title": "Database Schema Design", "type": "Backend"},
        {"id": 2, "title": "API Implementation", "type": "Backend"},
        {"id": 3, "title": "Frontend UI Components", "type": "Frontend"},
        {"id": 4, "title": "Integration Testing", "type": "QA"}
    ]
    
    return {
        "tasks": tasks,
        "status": "decomposed"
    }
