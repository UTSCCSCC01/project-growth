from datetime import datetime
from django import forms

from django.db import models

# Create your models here.
from users.models import User

#set up of courses
class CourseInfo(models.Model):
    #image = models.ImageField(upload_to='course/',)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="course name")
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

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    deadline = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    
    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

class BookCourse(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseInfo, on_delete=models.CASCADE) # null=True


class Upload(models.Model):

    id = models.BigAutoField(primary_key=True)
    remark = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')

    
    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)

class UploadBookUser(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

class Mark(models.Model):

    id = models.BigAutoField(primary_key=True)
    mark = models.CharField(max_length=5)
    
    def __str__(self):
        return self.mark

class UploadMark(models.Model):

    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)