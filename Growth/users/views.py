from django.shortcuts import render, redirect

from .forms import RegisterForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import BookCourse, CourseInfo, CourseUser,  Upload, UploadBookUser, Book


def register(request):

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:

        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    return render(request, 'index.html')


@login_required()
def app_home(request):
    return render(request, 'home.html', context={'data': request.user})


@login_required()
def dashboard(request):
    user_id = request.user.id
    role = request.user.role
    uploads = []
    upload_count = 0
    uploadBookUser = UploadBookUser.objects.filter(
        user_id=user_id)
    for uploadBook in uploadBookUser:
        uploads.append(Book.objects.get(id=uploadBook.book.id))
        upload_count = upload_count + 1

    queryset = BookCourse.objects.all()
    template_name = 'dashboard.html'
    if(role == 'Instructor' or role == 'Student'):
        count = CourseUser.objects.filter(user_id=int(user_id)).count()
        coursesUsers = CourseUser.objects.filter(user_id=int(user_id))
    else:
        coursesUsers = CourseInfo.objects.all()
        count = CourseInfo.objects.all().count()
    return render(request, template_name, {'books': queryset, 'courses': coursesUsers, 'count': count, 'upload_count': upload_count, 'uploads': uploads})


@login_required
def profile(request, slug):
    # return HttpResponse(slug)
    data = get_user_model().objects.filter(
        username=slug).first()
    return render(request, 'profile/user_profile.html', context={'user': request.user, 'data': data})


@login_required
def search_profile(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        data = get_user_model().objects.filter(
            username=searched).first()
        if(data != None):
            return render(request, 'profile/user_profile.html', context={'data': data})
        else:
            return redirect('/forum/')
    else:
        return redirect('/forum/')


@login_required
def edit_profile(request, slug):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            print(request.get_full_path())
            data = get_user_model().objects.filter(
                username=slug).first()
            return render(request, 'profile/user_profile.html', context={'data': data})
        else:
            return redirect('/')
    else:
        data = get_user_model().objects.filter(
            username=slug).first()
        form = EditProfileForm(instance=request.user)
        return render(request, 'profile/update_profile.html', context={'form': form, 'data': data})
