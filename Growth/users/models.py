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

    city = models.CharField(max_length=50, blank=True)

    description = models.CharField(max_length=100, blank=True)
    mobile_phone = models.IntegerField(blank=True)

    class Meta(AbstractUser.Meta):
        pass
