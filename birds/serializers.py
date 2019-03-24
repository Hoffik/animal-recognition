from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer to map the Project model instance for view."""

    class Meta:
        """Meta class to map Project serializer's fields with the model fields."""
        model = Project
        fields = ('id', 'name', 'directory', 'file_type', 'rights', 'tags', 'records') #identifications

