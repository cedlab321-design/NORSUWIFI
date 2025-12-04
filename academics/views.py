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


def school_calendar(request):
    # Static academic calendar milestones; replace with dynamic data if available
    calendar_items = [
        {"title": "Spring Registration Opens", "date": "Jan 8, 2026", "category": "Registration", "detail": "Enroll early to secure your classes and preferred schedules."},
        {"title": "Start of Classes", "date": "Feb 5, 2026", "category": "Instruction", "detail": "First day of regular classes for all programs."},
        {"title": "Midterm Exams", "date": "Mar 25-29, 2026", "category": "Exams", "detail": "Midterm assessment window. Confirm section-specific exam times with your instructor."},
        {"title": "Holiday Break", "date": "Apr 9-12, 2026", "category": "Holiday", "detail": "No classes. Offices operate on adjusted hours."},
        {"title": "Final Exams", "date": "May 20-27, 2026", "category": "Exams", "detail": "Final examination period. Check the posted exam schedule by course."},
        {"title": "Grades Posting Deadline", "date": "Jun 3, 2026", "category": "Grades", "detail": "Faculty deadline for submitting final grades."},
    ]
    return render(request, 'academics/calendar.html', {"calendar_items": calendar_items})
