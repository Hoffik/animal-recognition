from rest_framework import serializers
from .models import User, Project, Right, Tag, Record, Weight, Identification

class IdentificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    project = serializers.ReadOnlyField(source='tag.project.name')

    class Meta:
        model = Identification
        fields = ('id', 'user', 'record', 'tag', 'project', 'phase', 'created')

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'prior', 'project', 'image', 'identifications')

class RightSerializer(serializers.ModelSerializer):
    project = serializers.ReadOnlyField(source='project.id')
    user = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    identification_count = serializers.SerializerMethodField()
    role_name = serializers.CharField(source='get_role_display', required=False)
    # role_choices = serializers.SerializerMethodField()

    class Meta:
        model = Right
        fields = ('id', 'user', 'email', 'project', 'identification_count', 'role', 'role_name')

    def get_identifications(self, obj):
        identifications = Identification.objects.filter(user=obj.user, tag__project=obj.project)
        return IdentificationSerializer(identifications, many=True).data

    def get_identification_count(self, obj):
        return Identification.objects.filter(user=obj.user, tag__project=obj.project).count()

    def get_role_choices(self, obj):
        return Right.ROLE_CHOICES

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer to map the Project model instance for view."""
    file_type = serializers.CharField(source='get_file_type_display')
    rights = RightSerializer(many=True, read_only=True)
    role_names = serializers.SerializerMethodField()
    role_choices = serializers.SerializerMethodField()
    tag_count = serializers.SerializerMethodField()
    record_count = serializers.SerializerMethodField()
    record_with_file_count = serializers.SerializerMethodField()
    identification_count = serializers.SerializerMethodField()

    class Meta:
        """Meta class to map Project serializer's fields with the model fields."""
        model = Project
        fields = ('id', 'name', 'directory', 'file_type', 'rights', 'role_names', 'role_choices', 'tag_count', 'record_count', 'record_with_file_count', 'identification_count')

    def get_role_names(self, obj):
        return Right.ROLE_NAMES

    def get_role_choices(self, obj):
        return Right.ROLE_CHOICES

    def get_tag_count(self, obj):
        return Tag.objects.filter(project=obj).count()

    def get_record_count(self, obj):
        return Record.objects.filter(project=obj).count()

    def get_record_with_file_count(self, obj):
        return Record.objects.filter(project=obj, file_on_server=True).count()

    def get_identifications(self, obj):
        identifications = Identification.objects.filter(tag__in=obj.tags.all())
        return IdentificationSerializer(identifications, many=True).data

    def get_identification_count(self, obj):
        return Identification.objects.filter(tag__in=obj.tags.all()).count()
    
class UserSerializer(serializers.ModelSerializer):
    identifications = IdentificationSerializer(many=True, read_only=True)
    # identification_count = len(identifications)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'identifications', )