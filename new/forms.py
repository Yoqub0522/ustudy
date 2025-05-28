from django import forms

from new.models import Course, Student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name','description','start_date']

from cloudinary.uploader import upload

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name','age','course_name','email','image','video','file']

    def save(self, commit=True):
        instance = super().save(commit=False)

        image_file = self.files.get('image')
        if image_file:
            result = upload(image_file, resource_type='image')
            instance.image = result['public_id']

        video_file = self.files.get('video')
        if video_file:
            result = upload(video_file, resource_type='video')
            instance.video = result['public_id']

        file_file = self.files.get('file')
        if file_file:
            result = upload(file_file, resource_type='auto')
            instance.file = result['public_id']

        if commit:
            instance.save()
        return instance
