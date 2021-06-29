from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    
    instructor = models.BooleanField("Instructor",default=False)
    partner = models.BooleanField("Parner",default=False)

    class Meta(AbstractUser.Meta):
        pass


    
