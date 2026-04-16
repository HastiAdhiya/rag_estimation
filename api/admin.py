from django.contrib import admin
from .models import Project, Document, EstimationResult

admin.site.register(Project)
admin.site.register(Document)
admin.site.register(EstimationResult)
