from django.contrib import admin
from .models import CourseInfo, CourseUser, LessonInfo, Book, BookCourse

# Register your models here. to make them show on admin page
admin.site.register(CourseInfo)
admin.site.register(CourseUser)
admin.site.register(LessonInfo)
admin.site.register(Book)
admin.site.register(BookCourse)
