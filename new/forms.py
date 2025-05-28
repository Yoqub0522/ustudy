from django import forms

from new.models import Course, Student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','description','start_date']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields=['full_name','age','course_name','email','image','file']