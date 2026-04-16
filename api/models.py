from django.db import models
from django.contrib.auth.models import User
import uuid

class Project(models.Model):
    PRIORITY_CHOICES = [('H', 'High'), ('M', 'Medium'), ('L', 'Low')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    client_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    DOC_TYPES = [('REQ', 'Requirement'), ('HIST', 'Historical Data'), ('FEED', 'User Feedback')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=4, choices=DOC_TYPES, default='REQ')
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file.name} - {self.project.name}'

class EstimationResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='estimation')
    thread_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')
    effort_prediction = models.CharField(max_length=255, blank=True, null=True)
    confidence_score = models.FloatField(default=0.0)
    agent_logs = models.JSONField(default=dict, blank=True)
    recommended_team = models.TextField(blank=True, null=True)
    complexity_score = models.CharField(max_length=50, blank=True, null=True)
    generated_at = models.DateTimeField(auto_now=True)

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    estimated_hours = models.FloatField(default=0.0)
    
    def __str__(self):
        return f'{self.title} ({self.project.name})'

    def __str__(self):
        return f'Estimation for {self.project.name}'
