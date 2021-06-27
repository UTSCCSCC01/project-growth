from django import forms

from courses.models import CourseInfo


class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseInfo
        fields = ('name', 'description')
