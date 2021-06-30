from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', course_list, name='course_list'),
    url(r'^course_detail/(\d+)/$', course_detail, name='course_detail'),

    url(r'^addCourse/$', addCourse, name='addCourse'),
    url(r'^modCourse/', modCourse, name='modCourse'),
    url(r'^delCourse/', delCourse, name='delCourse'),
    url(r'^enrollCourse/', enrollCourse, name='enrollCourse'),
    url(r'^enrollOneCourse/', enrollOneCourse, name='enrollOneCourse'),
    url(r'^unenrollCourse/', unenrollCourse, name='unenrollCourse'),
]