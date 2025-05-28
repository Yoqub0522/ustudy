from django.contrib import admin

from new.models import Course


#
from new.models import  Course, Student

admin.site.register(Course)
admin.site.register(Student)

# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description','start_date')
#     list_filter = ('name',)
#     search_fields = ('name', 'description')
#     fields = ('name', 'start_date')
# admin.site.register(Course,CourseAdmin)
