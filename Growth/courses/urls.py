from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', course_list, name='course_list'),
    url(r'^course_detail/(\d+)/$', course_detail, name='course_detail'),
    url(r'^course_video/(\d+)/$', course_video, name='course_video'),
    url(r'^addCourse/$', addCourse, name='addCourse'),
    url(r'^modCourse/', modCourse, name='modCourse'),
    url(r'^delCourse/', delCourse, name='delCourse'),
]