from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm, CourseForm, UploadForm
from .models import BookCourse, CourseInfo,CourseUser, Book, Upload, UploadBookUser

from users.models import User
from .import models
from django.views.generic import TemplateView
# Create your views here.


def course_list(request):
    role = request.user.role
    user_id = request.user.id
    all_courses = []
    if(role == 'Instructor' or role == 'Student'):
        coursesUsers = CourseUser.objects.filter(user_id=int(user_id))
        for course in coursesUsers:
            all_courses.append(CourseInfo.objects.get(id=course.course_id))
    else:
        all_courses = CourseInfo.objects.all()
    return render(request, 'courses/course_list.html',{
        'all_courses':all_courses,
        'role':role,
    })

def course_detail(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        return render(request,'courses/course_detail.html', {
            'course':course
        })




def addCourse(request):
    if request.method == "GET":
        course_name_form = CourseForm()

        return render(request,'courses/addCourse.html',{

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
            courseUser = CourseUser.objects.create(
                course_id=courseInfo.id,
                user_id=request.user.id
            )
            courseUser.save()
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

def enrollCourse(request):
    user_id = request.user.id
    instructor_list = list(User.objects.filter(role="Instructor"))
    course_list = [] # all courses
    for instructor in instructor_list:
        courseUsers = list(CourseUser.objects.filter(user_id=instructor.id))
        for couU in courseUsers:
            course_list.append(CourseInfo.objects.get(id=couU.course_id))
    courseU = list(CourseUser.objects.filter(user_id=user_id)) #my chosen course
    mycourse_list = []
    for coU in courseU:
        mycourse_list.append(CourseInfo.objects.get(id=coU.course_id))
    for el in mycourse_list:
        course_list.remove(el)

    if request.method == "GET":
        return render(request, 'courses/enrollCourse.html',
                      {"all_courses":course_list})
    else:
        return redirect('/courses/')


def enrollOneCourse(request):
    nid = request.GET.get('nid')
    courseuser = CourseUser.objects.create(
        course_id=nid,
        user_id=request.user.id)
    courseuser.save()
    return redirect('/courses/')


def unenrollCourse(request):
    nid = request.GET.get('nid')
    bb = CourseUser.objects.get(course_id=nid,user_id=request.user.id)
    bb.delete()
    return redirect('/courses/')


















# NAMAN CODE




class Home(TemplateView):
    template_name = 'courses/book_list.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'courses/upload.html', context)


def book_list(request):

    role = request.user.role

    course_id = request.GET.get('nid')


    books = []

    if(role == 'Instructor' or role == 'Student' or role == 'Partner'):

        # Edited Portion



        bookCourse = BookCourse.objects.filter(course_id=course_id)

        for book in bookCourse:
            books.append(Book.objects.get(id=book.book_id))

    else:
        books = Book.objects.all()


        # Edited Portion
        
    return render(request, 'courses/book_list.html', {
            'books': books,
            'role':role,
            'course_id':course_id
            })





def upload_book(request):
    course_id = request.GET.get('nid')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():

            # Edit Portion
            # Working

            title = form.cleaned_data['title']
            deadline = form.cleaned_data['deadline']
            pdf = form.cleaned_data['pdf']
            cover = form.cleaned_data['cover']

            book = Book.objects.create(
                title = title,
                deadline = deadline,
                pdf = pdf,
                cover = cover
            )

            book.save()

            bookCourse = BookCourse.objects.create(

                book_id = book.id,
                course_id = course_id
                

            )

            bookCourse.save()

            # Till here

            # form.save()

            return redirect('/books/?nid='+course_id)
    else:
        
        form = BookForm()
        
        return render(request, 'courses/upload_book.html', {
        'form': form,
        'course_id':course_id,
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'courses/class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('courses/class_book_list')
    template_name = 'courses/upload_book.html'




# For student submission


def upload_list(request):


    
    role = request.user.role

    user_id = request.user.id

    book_id = request.GET.get('nid')


    uploads = []

    

    if(role == 'Instructor'):

        uploadBookUser = UploadBookUser.objects.filter(book_id=book_id)

        for uploadBook in uploadBookUser:
            uploads.append(Upload.objects.get(id=uploadBook.upload_id))

    elif(role == 'Student'):

        uploadBookUser = UploadBookUser.objects.filter(user_id=user_id).filter(book_id=book_id)

        for uploadBook in uploadBookUser:
           uploads.append(Upload.objects.get(id=uploadBook.upload_id)) 

    count = 0

    for upload in uploads:

        count = count + 1


            
    # elif(role == 'Student'):
        
        # uploadBookUser = UploadBookUser.objects.filter(user_id=user_id).filter(book_id=book_id)
        
        # for uploadBook in uploadBookUser:
            
            # uploads.append(Upload.objects.get(id=uploadBook.book_id)) 

        
    return render(request, 'courses/upload_list.html', {
            'uploads': uploads,
            'role':role,
            'book_id':book_id,
            'user_id':user_id,
            'count':count
            })


    

def upload_upload(request):

    book_id = request.GET.get('nid')

    user_id = request.user.id


    if request.method == 'POST':

        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            # Edit Portion
            # Working
            
            pdf = form.cleaned_data['pdf']

            upload = Upload.objects.create(
                
                remark = user_id,
                pdf = pdf
            )

            upload.save()

            uploadBookUser= UploadBookUser.objects.create(

                book_id = book_id,
                user_id = request.user.id,
                upload_id = upload.id
                

            )

            uploadBookUser.save()

            # Till here

            return redirect('/books/upload_l/?nid='+book_id)
    else:
        
        form = UploadForm()
        
        return render(request, 'courses/upload_upload.html', {
        'form': form,
        'book_id':book_id,
    })

def delete_upload(request, pk):
    if request.method == 'POST':
        upload = Upload.objects.get(pk=pk)
        upload.delete()
    return redirect('upload_list')