from .base import AgentState

def validator_agent(state: AgentState):
    """
    Critiques the estimation for consistency and missing risks.
    """
    estimations = state.get("estimations", {})
    
    feedback = []
    if not estimations:
        feedback.append("No estimations found to validate.")
    
    # Simple rule-based self-critique
    if "total_predicted_effort" in estimations:
        try:
            total = int(estimations["total_predicted_effort"].split()[0])
            if total < 20:
                feedback.append("The total effort seems unusually low for an end-to-end project.")
        except:
            pass

    return {
        "validator_feedback": feedback,
        "status": "validated"
    }
