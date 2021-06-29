from datetime import datetime

from django.db import models

# Create your models here.
from users.models import User


class CourseInfo(models.Model):
    #image = models.ImageField(upload_to='course/',)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="coursename")
    description = models.CharField(max_length=200, verbose_name="description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "coursename"
        verbose_name_plural = verbose_name


class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE)


class LessonInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name="chaptername")
    courseinfo = models.ForeignKey(CourseInfo, verbose_name="course info",on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "lession_name"
        verbose_name_plural = verbose_name


