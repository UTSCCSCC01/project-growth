from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)


    teacher = models.BooleanField
    partner = models.BooleanField




    class Meta(AbstractUser.Meta):
        pass
