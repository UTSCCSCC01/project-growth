from django import forms

from courses.models import CourseInfo, CourseUser, Assignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ('name', 'description')

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('cover','assignment', 'deadline', 'pdf')