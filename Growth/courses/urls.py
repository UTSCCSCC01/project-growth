from django.conf.urls import url
from django.urls import path, include
from . import views

from .views import *


urlpatterns = [
    
    path('', views.course_list, name='course_list'),
    path('course_detail/<int:pk>/', CourseDetail.as_view(), name='course_detail'),

    url(r'^addCourse/$', addCourse, name='addCourse'),
    url(r'^modCourse/', modCourse, name='modCourse'),
    url(r'^delCourse/', delCourse, name='delCourse'),
    url(r'^enrollCourse/', enrollCourse, name='enrollCourse'),
    url(r'^enrollOneCourse/', enrollOneCourse, name='enrollOneCourse'),
    url(r'^unenrollCourse/', unenrollCourse, name='unenrollCourse'),
    path('course_detail/<int:pk>/lectures/', include('forum.urls')),
    
]