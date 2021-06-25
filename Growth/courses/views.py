from django.shortcuts import render,redirect

from .forms import CourseForm
from .models import CourseInfo
from users.models import User
from .import models
# Create your views here.
def course_list(request):
    all_courses = CourseInfo.objects.all()
    all_users = User.objects.all()
    return render(request, 'courses/course_list.html',{
        'all_courses':all_courses,
        'all_users':all_users,
    })

def course_detail(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        return render(request,'courses/course_detail.html', {
            'course':course
        })

def course_video(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        return render(request,'courses/course_video.html', {
            'course':course
        })


def addCourse(request):
    if request.method == "GET":
        course_name_form = CourseForm()
        addCo = User.objects.all()
        return render(request,'courses/addCourse.html',{
            'addCo':addCo,
            'course_name_form':course_name_form,
        })
    else:
        course_name_form = CourseForm(request.POST)
        if course_name_form.is_valid():
            name = course_name_form.cleaned_data['name']
            description = course_name_form.cleaned_data['description']
            courseInfo = CourseInfo.objects.create(
                name=name,
                description=description)
            courseInfo.save()
            return redirect('/courses/')

def delCourse(request):
    nid = request.GET.get('nid')
    bb = CourseInfo.objects.get(id = nid)
    bb.delete()
    return redirect('/courses/')

def modCourse(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        course = CourseInfo.objects.get(id=nid)
        return render(request, 'courses/modCourse.html',{
            "course":course
        })
    else:
        nid = request.POST.get('id')
        name = request.POST.get('name')
        course = CourseInfo.objects.get(id=nid)
        course.name = name
        course.save()
        return redirect('/courses/')
