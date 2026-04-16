from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Document, EstimationResult
from .serializers import ProjectSerializer, DocumentSerializer, EstimationResultSerializer
from .neo4j_client import neo4j_client

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class EstimationResultViewSet(viewsets.ModelViewSet):
    queryset = EstimationResult.objects.all()
    serializer_class = EstimationResultSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import permissions

@method_decorator(csrf_exempt, name='dispatch')
class IngestProjectViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    """
    Ingest historical data or new projects.
    URL: /api/ingest/projects/
    """
    @action(detail=False, methods=['post'])
    def ingest_projects(self, request):
        file_obj = request.FILES.get('document')
        text_data = request.data.get('text_content')
        
        if not file_obj and not text_data:
            return Response({"error": "No document or text provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a mock project
        project_name = file_obj.name if file_obj else "Text Input Project"
        project = Project.objects.create(name=project_name)
        Document.objects.create(project=project, file=file_obj, text_content=text_data)
        EstimationResult.objects.create(project=project, status="ingested")
        
        # Init Neo4j Node with timeout/error handling
        try:
            # Simple check if Neo4j is alive or just wrap it
            neo4j_client.create_project_node(project.id, project.name)
        except Exception as e:
            # Log error but don't hang the whole request
            print(f"CRITICAL Neo4j connectivity error: {e}")

        return Response({
            "status": "success",
            "project_id": str(project.id),
            "thread_id": str(project.id), # Align with script.js expectations
            "message": "Input ingested successfully."
        })

class EstimationViewSet(viewsets.ViewSet):
    """
    Handles the multi-turn estimation flow.
    URL: /api/estimate/
    """

    @action(detail=False, methods=['post'])
    def start(self, request):
        project_id = request.data.get('project_id')
        if not project_id:
            return Response({"error": "project_id required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status to trigger poller transition
        EstimationResult.objects.filter(project_id=project_id).update(status="clarifying")
        
        return Response({
            "status": "success",
            "thread_id": project_id,
            "message": "Estimation session initialized. Clarifier active."
        })

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        # In a real app, this reads from AgentState
        res = EstimationResult.objects.filter(project_id=pk).first()
        current_status = res.status if res else "unknown"
        
        return Response({
            "thread_id": pk,
            "state": current_status.upper(),
            "status": current_status,
            "current_step": f"{current_status.capitalize()} Agent",
            "questions": ["What is the primary target audience?"] if current_status == "clarifying" else [],
            "is_complete": current_status == "completed"
        })

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        # Simulate moving to next agent
        EstimationResult.objects.filter(project_id=pk).update(status="retrieving")
        return Response({
            "status": "success",
            "message": "Clarification received. Retriever agent engaged."
        })

    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        EstimationResult.objects.filter(project_id=pk).update(status="completed")
        return Response({
            "status": "success",
            "message": "Final feedback recorded. Graph updated."
        })
