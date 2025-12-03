# academics/views.py
from django.shortcuts import render, get_object_or_404
from .models import Department, Course

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'academics/department_list.html', {'departments': departments})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    courses = Course.objects.filter(department=department)
    return render(request, 'academics/department_detail.html', {
        'department': department,
        'courses': courses
    })

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'academics/course_detail.html', {'course': course})