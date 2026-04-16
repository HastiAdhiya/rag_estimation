import os
import django
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Project, Document, EstimationResult
from api.neo4j_client import Neo4jClient

neo4j_client = Neo4jClient()

def seed():
    print("Starting data seeding...")
    
    # Project 1: E-commerce Platform
    p1 = Project.objects.create(
        name="Global E-commerce Hub",
        priority="H",
        client_name="RetailGlobal Corp"
    )
    doc1 = Document.objects.create(
        project=p1,
        title="SRS - E-commerce",
        text_content="A full-featured e-commerce platform with cart, checkout, payment integration (Stripe), and admin dashboard. Estimated effort: 450 hours.",
        doc_type="Historical"
    )
    # Result 1
    EstimationResult.objects.create(
        project=p1,
        total_effort="450 Hours",
        confidence_score=0.92,
        summary="Complete e-commerce rollout including mobile responsive frontend.",
        is_complete=True
    )
    neo4j_client.create_project_node(p1.id, p1.name)
    print(f"Seeded Project 1: {p1.name}")

    # Project 2: Banking Mobile App
    p2 = Project.objects.create(
        name="SecureBank Mobile",
        priority="H",
        client_name="SecureBank Int"
    )
    doc2 = Document.objects.create(
        project=p2,
        title="Requirement - Mobile Banking",
        text_content="Mobile app for iOS and Android. Features: biometrics, transaction history, funds transfer, and MFA. Estimated effort: 1200 hours.",
        doc_type="Historical"
    )
    # Result 2
    EstimationResult.objects.create(
        project=p2,
        total_effort="1200 Hours",
        confidence_score=0.88,
        summary="High-security banking application with multiple third-party integrations.",
        is_complete=True
    )
    neo4j_client.create_project_node(p2.id, p2.name)
    print(f"Seeded Project 2: {p2.name}")

    print("Seeding complete.")

if __name__ == "__main__":
    seed()
