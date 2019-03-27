from django.db import models
from django.core.validators import validate_slug
from .validators import KeywordValidator
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username

class Project(models.Model):
    """Animal recognition project"""
    name = models.CharField(max_length=50)
    directory = models.CharField(max_length=50, validators=[validate_slug, KeywordValidator(keyword_list=["admin", "rest_api"])], unique=True)
    phase = models.IntegerField(default=1, blank=True)  # Crowdsourcing input iteration. Each crowdsourcing input follows a machine learning iteration.
    FILE_TYPE_CHOICES = (
        ('i', 'image'),
        ('a', 'audio'),
        ('v', 'video'),
    )
    file_type = models.CharField(
        max_length=1,
        choices=FILE_TYPE_CHOICES
    )   

    def __str__(self):
        return self.name

class Right(models.Model):
    """User rights for each project"""
    user = models.ForeignKey(
        User,
        related_name='rights',
        on_delete=models.CASCADE,
        null=True,  # Temporary until user login implemented
        blank=True
    )
    project = models.ForeignKey(
        Project,
        related_name='rights',
        on_delete=models.CASCADE
    )
    ROLE_CHOICES = (
        (0, 'owner'),
        (1, 'expert'),
        (2, 'layman'),
    )
    role = models.IntegerField(
        choices=ROLE_CHOICES,
        default=2,
        blank=True
    )

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return self.user + '_' + self.project + '_' + str(self.role)

class Tag(models.Model):
    """Choices (most often animal species names or 'noice') for each recording"""
    name = models.CharField(max_length=50)
    prior = models.IntegerField(default=1)  # Default weight. If no weight for given Record is available, prior is used.
    project = models.ForeignKey(
        Project,
        related_name='tags',
        on_delete=models.CASCADE
    )

    def tag_images_path(instance, filename):
        return 'tag_images/' + instance.project.directory + '/' + filename

    image = models.ImageField(upload_to=tag_images_path, null=True, blank=True)

    def __str__(self):
        return self.name

class Record(models.Model):
    """Records of animals in image, audio or video format"""
    filename = models.CharField(max_length=50)
    file_on_server = models.BooleanField()
    importance = models.IntegerField(default=1) # Influences probability of record selection. Input for weighted random selection.
    project = models.ForeignKey(
        Project,
        related_name='records',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.filename

class Weight(models.Model):
    """Record weights for each tag. If no weight for a Tag is available, prior is used."""
    record = models.ForeignKey(
        Record,
        related_name='weights',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        related_name='weights',
        on_delete=models.CASCADE
    )
    value = models.IntegerField(default=1) # Determines the order of presented tags for selected record.

    class Meta:
        unique_together = ('record', 'tag',)

    def __str__(self):
        return str(self.record) + '_' + str(self.tag) + '_' + str(self.value)


class Identification(models.Model):
    """Animal recognition entry"""
    user = models.ForeignKey(
        User,
        related_name='identifications',
        on_delete=models.CASCADE,
        null=True,  #Temporary until user login implemented
        blank=True
    )
    record = models.ForeignKey(
        Record,
        related_name='identifications',
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        related_name='identifications',
        on_delete=models.CASCADE
    )
    phase = models.IntegerField()  # Crowdsourcing input iteration. Each crowdsourcing input follows a machine learning iteration.
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + '_' + str(self.record) + '_' + str(self.tag)