from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    nickname = models.CharField(max_length=50, blank=True)

    ROLE_CHOICES = (
        ('Partner', 'Partner'), ('Student',
                                 'Student'), ('Instructor', 'Instructor'),
    )
    role = models.CharField(
        max_length=20, default='---Select Role---', choices=ROLE_CHOICES)

    class Meta(AbstractUser.Meta):
        pass


class Role(models.Model):

    ROLE_CHOICES = (
        ('Partner', 'Partner'), ('Student',
                                 'Student'), ('Instructor', 'Instructor'),
    )
    role = models.CharField(
        max_length=20, default='---Select Role---', choices=ROLE_CHOICES)
