import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Project, Document, EstimationResult

def seed_one():
    print("Seeding 1 historical project...")
    p = Project.objects.create(
        name="Legacy Inventory System",
        priority="M",
        client_name="OldCorp Logistics"
    )
    Document.objects.create(
        project=p,
        title="Inventory Specs",
        text_content="A monolithic inventory management system with SOAP API and Oracle DB. Total effort: 850 hours.",
        doc_type="Historical"
    )
    EstimationResult.objects.create(
        project=p,
        total_effort="850 Hours",
        confidence_score=0.95,
        summary="Detailed inventory management migration.",
        status="completed",
        is_complete=True
    )
    print(f"Success: Seeded {p.name}")

if __name__ == "__main__":
    seed_one()
