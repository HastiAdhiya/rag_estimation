from celery import shared_task
from .agents.base import create_mage_graph
from .models import EstimationResult

@shared_task
def run_estimation_workflow(project_id: str, current_status: str, user_response: str = None):
    # Initialize state graph
    mage_app = create_mage_graph()
    
    # Configuration - mock config for thread_id
    config = {"configurable": {"thread_id": project_id}}
    
    # State setup based on status
    if current_status == "clarifying":
        # Initial run
        initial_state = {
            "project_id": project_id,
            "requirements": "", # This would ideally be loaded from Document model
            "clarification_questions": [],
            "tasks": [],
            "estimations": {},
            "validator_feedback": [],
            "status": current_status,
            "thread_id": project_id
        }
        
        for event in mage_app.stream(initial_state, config):
            for k, v in event.items():
                print(f"Agent {k} completed.")
                new_status = v.get("status")
                if new_status:
                    EstimationResult.objects.filter(project_id=project_id).update(status=new_status)
    else:
        # Resume with user answers
        # For simplicity, if we were at clarification we now just push it through
        # In actual implementation you might update the state or stream again
        # Assuming current_status == 'retrieving' implies we should resume
        EstimationResult.objects.filter(project_id=project_id).update(status="completed")

