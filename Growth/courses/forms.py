from django import forms

from courses.models import CourseInfo, CourseUser, Book


class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ('name', 'description')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'deadline', 'pdf', 'cover')