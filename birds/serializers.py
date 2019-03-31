from rest_framework import serializers
from .models import User, Project, Right, Tag, Record, Weight, Identification

class IdentificationSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Identification
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    """Serializer to map the Tag model instance for view."""

    class Meta:
        """Meta class to map Tag serializer's fields with the model fields."""
        model = Tag
        fields = ('id', 'name', 'prior', 'project', 'image', 'identifications')

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer to map the Project model instance for view."""
    file_type = serializers.CharField(source='get_file_type_display')
    tags = TagSerializer(many=True, read_only=True)
    identifications = serializers.SerializerMethodField()

    class Meta:
        """Meta class to map Project serializer's fields with the model fields."""
        model = Project
        fields = ('id', 'name', 'directory', 'file_type', 'rights', 'tags', 'records', 'identifications')

    def get_identifications(self, obj):
        identifications = Identification.objects.filter(tag__in=obj.tags.all())
        # comments = Comments.objects.filter(track__album_id=obj.pk)
        return IdentificationSerializer(identifications, many=True).data
    
class UserSerializer(serializers.ModelSerializer):
    identifications = IdentificationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'identifications')