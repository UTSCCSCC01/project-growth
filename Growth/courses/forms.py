from django import forms
from django.forms import widgets

from courses.models import CourseInfo, CourseUser, Book, Upload, Mark

class DateInput(forms.DateInput):
    input_type = 'date'


    

class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ('name', 'description')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'deadline', 'pdf', 'cover')
        widgets = {'deadline' : DateInput()}

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('pdf',)

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('mark',)
