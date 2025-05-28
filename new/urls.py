from django.urls import path

from new.views import create_course, course_list, create_student, student_list, get_student_detail, student_update, \
    delete_student, get_course_detail, course_update, delete_course, filter_by_course,export_to_xslx

urlpatterns = [
    path('', course_list, name='course-list'),
    path('courses/create/', create_course, name='course-create'),
    path('student/list/', student_list, name='student-list'),
    path('student/create/', create_student, name='student-create'),
    path('student/detail/<int:pk>/', get_student_detail, name='student-detail'),
    path('student/update/<int:pk>/', student_update, name='student-update'),
    path('student/delete/<int:pk>/', delete_student, name='student-delete'),
    # course crud
    path('course/detail/<int:pk>/', get_course_detail, name='course-detail'),
    path('course/update/<int:pk>/', course_update, name='course-update'),
    path('course/delete/<int:pk>/', delete_course, name='course-delete'),
    path('course/filter', filter_by_course, name='filter'),
    path('excel/', export_to_xslx, name='excel'),


]