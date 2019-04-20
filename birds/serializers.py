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
    # project = serializers.ReadOnlyField(source='project.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    project_dir = serializers.ReadOnlyField(source='project.directory')
    identification_count = serializers.SerializerMethodField()
    role_name = serializers.ReadOnlyField(source='get_role_display')
    # role_choices = serializers.SerializerMethodField()

    class Meta:
        model = Right
        fields = ('id', 'user', 'username', 'email', 'project', 'project_dir', 'identification_count', 'role', 'role_name')

    def get_identifications(self, obj):
        identifications = Identification.objects.filter(user=obj.user, tag__project=obj.project)
        return IdentificationSerializer(identifications, many=True).data

    def get_identification_count(self, obj):
        return Identification.objects.filter(user=obj.user, tag__project=obj.project).count()

    def get_role_choices(self, obj):
        return Right.ROLE_CHOICES
    
class UserSerializer(serializers.ModelSerializer):
    # identifications = IdentificationSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

class BasicProjectSerializer(serializers.ModelSerializer):
    """Serializer to map basic Project model data for project list view."""
    current_user_right = serializers.SerializerMethodField()
    file_type = serializers.CharField(source='get_file_type_display')
    right_count = serializers.SerializerMethodField()
    tag_count = serializers.SerializerMethodField()
    record_count = serializers.SerializerMethodField()
    identification_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'directory', 'current_user_right', 'file_type', 'right_count', 'tag_count', 'record_count', 'identification_count',)

    def get_current_user_right(self, obj):
        try:
            return Right.objects.get(project=obj, user=self.context['request'].user.id).get_role_display()
        except:
            return None

    def get_right_count(self, obj):
        return Right.objects.filter(project=obj).count()

    def get_tag_count(self, obj):
        return Tag.objects.filter(project=obj).count()

    def get_record_count(self, obj):
        return Record.objects.filter(project=obj).count()

    def get_identification_count(self, obj):
        return Identification.objects.filter(tag__in=obj.tags.all()).count()


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer to map the Project model instance for view."""
    directory = serializers.ReadOnlyField()
    file_type = serializers.CharField(source='get_file_type_display', read_only=True)
    rights = RightSerializer(many=True, read_only=True)
    owners = serializers.SerializerMethodField()
    role_names = serializers.SerializerMethodField()
    # role_choices = serializers.SerializerMethodField()
    right_count = serializers.SerializerMethodField()
    owner_count = serializers.SerializerMethodField()
    expert_count = serializers.SerializerMethodField()
    layman_count = serializers.SerializerMethodField()
    current_user_right = serializers.SerializerMethodField()
    users_wo_rights = serializers.SerializerMethodField()
    tag_count = serializers.SerializerMethodField()
    record_count = serializers.SerializerMethodField()
    record_with_file_count = serializers.SerializerMethodField()
    identification_count = serializers.SerializerMethodField()

    class Meta:
        """Meta class to map Project serializer's fields with the model fields."""
        model = Project
        fields = ('id', 'name', 'directory', 'file_type', 'rights', 'owners', 'role_names', 'right_count', 'owner_count', 'expert_count', 'layman_count', 'current_user_right', 'users_wo_rights', 'tag_count', 'record_count', 'record_with_file_count', 'identification_count')

    # Use this method for the custom field
    def get_current_user_right(self, obj):
        # result = None
        try:
            return Right.objects.get(project=obj, user=self.context['request'].user.id).get_role_display()
        except:
            return None
        # return result
        # return Right.objects.filter(project=obj, user=self.context['request'].user.id).values_list('role', flat=True)
        # return Right.objects.get(project=obj, user=self.context['request'].user.id).get_role_display()

    def get_owners(self, obj):
        return Right.objects.filter(project=obj, role=0).values_list('user_id', flat=True)

    def get_role_names(self, obj):
        return Right.ROLE_NAMES

    def get_role_choices(self, obj):
        return Right.ROLE_CHOICES

    def get_right_count(self, obj):
        return Right.objects.filter(project=obj).count()

    def get_owner_count(self, obj):
        return Right.objects.filter(project=obj, role=0).count()

    def get_expert_count(self, obj):
        return Right.objects.filter(project=obj, role=1).count()

    def get_layman_count(self, obj):
        return Right.objects.filter(project=obj, role=2).count()

    def get_users_wo_rights(self, obj):
        users = User.objects.exclude(rights__in=obj.rights.all())
        return UserSerializer(users, many=True).data

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
