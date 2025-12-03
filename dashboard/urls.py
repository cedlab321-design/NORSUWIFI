# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    # Student area
    path('student/', views.student_dashboard, name='student_index'),
    path('student/courses/', views.student_courses, name='student_courses'),
    path('student/course/<slug:slug>/', views.student_course_detail, name='student_course_detail'),
    path('student/course/<slug:slug>/join/', views.student_join_course, name='student_join_course'),
    path('student/course/<slug:slug>/leave/', views.student_leave_course, name='student_leave_course'),
    path('student/assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('student/assignment/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('student/assignments/', views.student_assignments, name='student_assignments'),
    path('student/grades/', views.student_grades, name='student_grades'),

    # Staff area
    path('staff/', views.staff_dashboard, name='staff_index'),
    path('staff/students/', views.staff_student_management, name='staff_student_management'),
    path('staff/support/', views.staff_support_tools, name='staff_support_tools'),
    # Staff student management actions
    path('staff/students/list/', views.staff_students_list, name='staff_students_list'),
    path('staff/students/<int:user_id>/edit/', views.staff_edit_student, name='staff_edit_student'),
    path('staff/students/<int:user_id>/reset-password/', views.staff_reset_password, name='staff_reset_password'),
    path('staff/students/<int:user_id>/enroll/<slug:slug>/', views.staff_enroll_student, name='staff_enroll_student'),
    path('staff/students/<int:user_id>/unenroll/<slug:slug>/', views.staff_unenroll_student, name='staff_unenroll_student'),
    path('staff/students/<int:user_id>/performance/', views.staff_view_performance, name='staff_view_performance'),

    # Support tools: tickets, announcements, documents
    path('staff/support/tickets/', views.tickets_list, name='tickets_list'),
    path('staff/support/tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('staff/support/announcements/', views.announcements_list, name='announcements_list'),
    path('staff/support/announcements/new/', views.announcement_create, name='announcement_create'),
    path('staff/support/documents/', views.documents_list, name='documents_list'),
    path('staff/support/documents/upload/', views.document_upload, name='document_upload'),

    # Faculty area
    path('faculty/', views.faculty_dashboard, name='faculty_index'),
    path('faculty/course-builder/', views.faculty_course_builder, name='faculty_course_builder'),
    path('faculty/grade-submissions/', views.faculty_grade_submissions, name='faculty_grade_submissions'),
    path('faculty/staff-coordination/', views.faculty_staff_coordination, name='faculty_staff_coordination'),
    # Faculty course builder actions
    path('faculty/courses/', views.faculty_courses_list, name='faculty_courses_list'),
    path('faculty/courses/new/', views.faculty_course_create, name='faculty_course_create'),
    path('faculty/courses/<slug:slug>/edit/', views.faculty_course_edit, name='faculty_course_edit'),
    path('faculty/courses/<slug:slug>/materials/', views.faculty_course_materials, name='faculty_course_materials'),

    # Faculty grading actions
    path('faculty/grade-submissions/list/', views.faculty_grade_submissions_list, name='faculty_grade_submissions_list'),
    path('faculty/grade-submissions/<int:submission_id>/grade/', views.faculty_grade_submission, name='faculty_grade_submission'),

    # Faculty staff coordination
    path('faculty/staff-tasks/', views.faculty_staff_tasks, name='faculty_staff_tasks'),
    path('faculty/staff-notes/', views.faculty_staff_notes, name='faculty_staff_notes'),
]