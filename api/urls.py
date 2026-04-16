from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, DocumentViewSet, EstimationResultViewSet, IngestProjectViewSet, EstimationViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'estimations', EstimationResultViewSet)
router.register(r'estimate', EstimationViewSet, basename='estimate')
router.register(r'ingest', IngestProjectViewSet, basename='ingest')

urlpatterns = [
    path('', include(router.urls)),
]
