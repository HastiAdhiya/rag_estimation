from .base import AgentState

def estimator_agent(state: AgentState):
    """
    Calculates hours for tasks based on historical analogies and rules.
    """
    tasks = state.get("tasks", [])
    
    estimations = {}
    total_hours = 0
    
    for task in tasks:
        # Placeholder calculation logic
        hours = 8 if task["type"] == "Backend" else 6
        estimations[task["title"]] = f"{hours} hours"
        total_hours += hours
        
    estimations["total_predicted_effort"] = f"{total_hours} hours"
    
    return {
        "estimations": estimations,
        "status": "estimated"
    }
