from rest_framework import serializers
from .models import Project, Document, EstimationResult

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class EstimationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimationResult
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    estimation = EstimationResultSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
