from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from user.utils import checking_user, checking_role
from .forms import CourseForm, StudentForm
from .models import Course, Student
from django.db.models import Q


def course_list(request):
    courses = Course.objects.all()


    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    if q != '':
        courses=courses.filter(Q(name__icontains=q)|Q(description__icontains=q))

    context = {
        'courses': courses,
        'user': request.user
    }

    return render(request, 'course_list.html', context)

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})


from django.core.paginator import Paginator

from django.db.models import Q



def student_list(request):
    students = Student.objects.all().order_by('-registration_date')
    q = request.GET.get('q') or ''

    if q:
        students = students.filter(Q(full_name__icontains=q) | Q(email__icontains=q))

    paginator = Paginator(students, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'q': q,
        'is_paginated': page_obj.has_other_pages()
    })


def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm()
    return render(request, 'create_student.html', {'form': form})

def get_student_detail(request, pk):
    student = Student.objects.get(pk=pk)
    context={
        'student':student
    }
    return render(request, 'student_detail.html', {'student':student})

def student_update(request, pk):
    student=Student.objects.get(pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST,request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'create_student.html', {'form': form})


def delete_student(request,pk):
    student=Student.objects.get(pk=pk)
    if request.method=='POST':
        student.delete()
        return redirect('student-list')
    return render(request,'delete_student.html',{'student':student})


def get_course_detail(request, pk):
    course = Course.objects.get(pk=pk)
    context={
        'course':course
    }
    return render(request, 'course_detail.html', {'course':course})


def course_update(request, pk):
    course=Course.objects.get(pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'create_course.html', {'form': form})


def delete_course(request,pk):
    course=Course.objects.get(pk=pk)
    if request.method=='POST':
        course.delete()
        return redirect('course-list')
    return render(request,'delete_course.html',{'course':course})


from django.shortcuts import render
from .models import Course, Student


def filter_by_course(request):
    courses = Course.objects.all()
    selected_course = request.GET.get('course_id')
    students = []

    if selected_course:

        students = Student.objects.filter(course_name_id=selected_course)

    context = {
        'courses': courses,
        'students': students,
        'selected_course': selected_course
    }
    return render(request, 'filter_students.html', context)
import openpyxl
from django.http import HttpResponse
def export_to_xslx(request):
    workbook=openpyxl.Workbook()
    sheet=workbook.active
    sheet.title="new"
    sheet.append([

        'Nomi',
        'Malumot',
        'boshlangam vaqt',
        'action'

    ])
    musics=Course.objects.all()
    for music in musics:
        sheet.append([
            music.name,
            music.description,
            music.start_date,
        ])
    response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition']='attachment;filename="kitoblar.xlsx"'
    workbook.save(response)
    return response



