from datetime import datetime

from django.db import models

# Create your models here.
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

class LessonInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name="chaptername")
    courseinfo = models.ForeignKey(CourseInfo, verbose_name="course info",on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "lession_name"
        verbose_name_plural = verbose_name


class VideoInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name="videoname")
    study_time = models.IntegerField(default=0, verbose_name="study_time")
    url = models.URLField(default='https://www.utoronto.ca/',verbose_name="movie link",max_length=200)
    lessoninfo = models.ForeignKey(LessonInfo, on_delete=models.CASCADE, verbose_name="lessoninfo")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="add time" )


    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "video_name"
        verbose_name_plural = verbose_name

class SourceInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name="resourcename")
    downloads = models.FileField(upload_to='source/',max_length=200,verbose_name="downloadpath")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="add time" )
    course_info = models.ForeignKey(CourseInfo,on_delete=models.CASCADE,verbose_name="Course")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "resource"
        verbose_name_plural = verbose_name