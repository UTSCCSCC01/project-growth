from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm, CourseForm, UploadForm, MarkForm
from .models import BookCourse, CourseInfo,CourseUser, Book, Upload, UploadBookUser, Mark, UploadMark

from users.models import User
from .import models
from django.views.generic import TemplateView

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

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
    return render(request, 'courses/course_list.html', {
        'all_courses': all_courses,
        'role': role,
    })


class CourseList(ListView):
    model = CourseInfo
    template_name = 'courses/course_list.html'  # <appName>/<model>_<viewtype>.html
    context_object_name = 'course'

    # this will be minipulated when using filters,
    # the minus means decending order
    # Change this ordering to by likes when you sort by best
    #ordering = ['-date_posted']


class CourseDetail(DetailView):
    model = CourseInfo
    template_name = 'courses/course_detail.html'  # <appName>/<model>_<viewtype>.html
    context_object_name = 'course'

    # this will be minipulated when using filters,
    # the minus means decending order
    # Change this ordering to by likes when you sort by best
    #ordering = ['-date_posted']


def course_detail(request, course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        return render(request, 'courses/course_detail.html', {
            'course': course
        })


def addCourse(request):
    if request.method == "GET":
        course_name_form = CourseForm()

        return render(request, 'courses/addCourse.html', {

            'course_name_form': course_name_form,
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
    bb = CourseInfo.objects.get(id=nid)
    bb.delete()
    return redirect('/courses/')


def modCourse(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        course = CourseInfo.objects.get(id=nid)
        return render(request, 'courses/modCourse.html', {
            "course": course
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
    course_list = []  # all courses
    for instructor in instructor_list:
        courseUsers = list(CourseUser.objects.filter(user_id=instructor.id))
        for couU in courseUsers:
            course_list.append(CourseInfo.objects.get(id=couU.course_id))
    courseU = list(CourseUser.objects.filter(
        user_id=user_id))  # my chosen course
    mycourse_list = []
    for coU in courseU:
        mycourse_list.append(CourseInfo.objects.get(id=coU.course_id))
    for el in mycourse_list:
        course_list.remove(el)

    if request.method == "GET":
        return render(request, 'courses/enrollCourse.html',
                      {"all_courses": course_list})
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
    bb = CourseUser.objects.get(course_id=nid, user_id=request.user.id)
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
    course_from_id = CourseInfo.objects.get(id=course_id)
    #posts = Post.objects.get(course=course_from_id)
    # print(posts)
    # Query posts get all by course id
    # in html just include the forum thing

    books = []

    if(role == 'Instructor' or role == 'Student' or role == 'Partner'):

        # Edited Portion

        bookCourse = BookCourse.objects.filter(course_id=course_id)
        course = get_object_or_404(CourseInfo, id=course_id)

        for book in bookCourse:
            books.append(Book.objects.get(id=book.book_id))

    else:
        books = Book.objects.all()
        course = None

        # Edited Portion

    return render(request, 'courses/book_list.html', {
        'books': books,
        'role': role,
        'course_id': course_id,
        'course': course,
        'posts': course_from_id.post_set.all,
    })


def upload_book(request):
    course_id = request.GET.get('nid')
    course = get_object_or_404(CourseInfo, id=course_id)

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
                title=title,
                deadline=deadline,
                pdf=pdf,
                cover=cover
            )

            book.save()

            bookCourse = BookCourse.objects.create(

                book_id=book.id,
                course_id=course_id


            )

            bookCourse.save()

            # Till here

            # TODO: @NAMAN to check if you need the following line
            # form.save()

            return redirect('/books/?nid='+course_id)
    else:

        form = BookForm()

        return render(request, 'courses/upload_book.html', {
            'form': form,
            'course_id': course_id,
            'course': course
        })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)

        cid = BookCourse.objects.get(book_id=book.id)

        c_id = cid.course_id

        book.delete()
    return redirect('/books/?nid='+str(c_id))


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

    # uploadmarks = UploadMark.objects.filter()

    uploads = []

    all_marks = Mark.objects.all()

    k = 0

    for j in all_marks:
        k = k + 1

    marks = []


    if(role == 'Instructor'):

        uploadBookUser = UploadBookUser.objects.filter(book_id=book_id)


        for uploadBook in uploadBookUser:
            uploads.append(Upload.objects.get(id=uploadBook.upload_id))



    elif(role == 'Student'):

        uploadBookUser = UploadBookUser.objects.filter(
            user_id=user_id).filter(book_id=book_id)



        for uploadBook in uploadBookUser:

           uploads.append(Upload.objects.get(id=uploadBook.upload_id))


           if(k>0):

               uploadmarks = UploadMark.objects.filter(upload_id=uploadBook.upload_id)
               for um in uploadmarks:
                   marks.append(Mark.objects.get(id=um.mark_id))

        index = [0]

        for nb in marks:
            index.append(nb.id)
            #print(nb.id)

        maximum_index = max(index)

        if(maximum_index != 0):
            for jj in marks:
                if(maximum_index == jj.id):
                    marks.clear()
                    marks.append(jj)


    count = 0

    for upload in uploads:

        count = count + 1

    book_obj = get_object_or_404(Book, id=book_id)



    c = 0

    for m in marks:

        c = c + 1



    # elif(role == 'Student'):

    # uploadBookUser = UploadBookUser.objects.filter(user_id=user_id).filter(book_id=book_id)

    # for uploadBook in uploadBookUser:

    # uploads.append(Upload.objects.get(id=uploadBook.book_id))

    return render(request, 'courses/upload_list.html', {

            'uploads': uploads,
            'role':role,
            'book_id':book_id,
            'user_id':user_id,
            'count':count,
            'book': book_obj,
            'c': c,
            'marks':marks,

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
                pdf = pdf,

            )

            upload.save()


            uploadBookUser= UploadBookUser.objects.create(

                book_id=book_id,
                user_id=request.user.id,
                upload_id=upload.id


            )

            uploadBookUser.save()

            # Save Form for Marks



            # Till here

            return redirect('/books/upload_l/?nid='+book_id)
    else:

        form = UploadForm()

        return render(request, 'courses/upload_upload.html', {
            'form': form,
            'book_id': book_id,
        })



def delete_upload(request, pk):
    if request.method == 'POST':
        upload = Upload.objects.get(pk=pk)

        njid = UploadBookUser.objects.get(upload_id=upload.id)

        nj_id = njid.book_id

        upload.delete()

    return redirect('/books/upload_l/?nid='+str(nj_id))


# Upload mark should be same as upload_upload

def upload_mark(request):

    upload_id = request.GET.get('nid')



    uploadbookUser = UploadBookUser.objects.get(upload_id=upload_id)

    book_id = uploadbookUser.book_id



    if request.method == 'POST':

        form = MarkForm(request.POST, request.FILES)

        if form.is_valid():

            mark = form.cleaned_data['mark']

            markobject = Mark.objects.create(

                mark = mark,
            )


            markobject.save()



            uploadMark = UploadMark.objects.create(

                mark_id = markobject.id,
                upload_id = upload_id,
                book_id = book_id,
            )

            uploadMark.save()




            ubu_object = UploadBookUser.objects.get(upload_id=upload_id)

            ubu_object_bookid = ubu_object.book_id



            return redirect('/books/upload_l/?nid='+str(ubu_object_bookid))
    else:

        form = MarkForm()

        return render(request, 'courses/upload_mark.html', {
        'form': form,
        'upload_id':upload_id,
        })


def result(request):



    role = request.user.role

    user_id = request.user.id

    book_id = request.GET.get('nid')



    uploadMark = UploadMark.objects.filter(book_id=book_id)

    upload_list = []

    max_mm = "Not Applicable"
    min_mm = "Not Applicable"
    mean_mm = "Not Applicable"


    for umu in uploadMark:

        upload_umu = umu.upload_id

        if upload_umu not in upload_list:
            upload_list.append(upload_umu)


    marks_marks = []

    for umuu in upload_list:

        uploadmarkUser = UploadMark.objects.filter(book_id=book_id).filter(upload_id=umuu)

        marks_m = []

        for umuu_m in uploadmarkUser:

              marks_m.append(Mark.objects.get(id=umuu_m.mark_id))

        index_m = []

        for jnjb in marks_m:

            index_m.append(jnjb.id)

        maximum_index_m = max(index_m)

        for njbj in marks_m:
            if(maximum_index_m == njbj.id):
                marks_m.clear()
                marks_marks.append(njbj)

        marks_value = []

        for ma_ma in marks_marks:
            marks_value.append(int(ma_ma.mark))




        if(len(marks_value)>0):
            max_mm = max(marks_value)
            min_mm = min(marks_value)
            sum_mm = sum(marks_value)
            mean_mm = sum_mm/len(marks_value)




    return render(request, 'courses/result.html', {

            'role':role,
            'book_id':book_id,
            'user_id':user_id,
            'marks_marks':marks_marks,
            'max_mm':max_mm,
            'min_mm':min_mm,
            'mean_mm':mean_mm,

            })

