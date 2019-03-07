from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username

class Bird(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Recording(models.Model):
    filename = models.CharField(max_length=50)
    note = models.CharField(max_length=50, default="", blank=True)
    weight = models.IntegerField(default=1)
    has_file = models.BooleanField(default=False)
    option_1 = models.ForeignKey(
        Bird,
        related_name='no1_recordings',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    option_2 = models.ForeignKey(
        Bird,
        related_name='no2_recordings',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.filename

class Evaluation(models.Model):
    user = models.ForeignKey(
        User,
        related_name='evaluations',
        on_delete=models.CASCADE,
        null=True,  #Temporary until user login implemented
        blank=True
    )
    recording = models.ForeignKey(
        Recording,
        related_name='evaluations',
        on_delete=models.CASCADE
    )
    bird = models.ForeignKey(
        Bird,
        related_name='evaluations',
        on_delete=models.CASCADE
    )