# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import (
    Course, Enrollment, Assignment, Submission, Grade,
    Ticket, Announcement, Document, StaffTask, StaffNote,
)
from .forms import (
    SubmissionForm, StudentEditForm, TicketForm, AnnouncementForm, DocumentUploadForm,
    CourseForm, AssignmentForm, GradeForm, StaffTaskForm, StaffNoteForm,
)
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods

User = get_user_model()

# Faculty: course builder and grading
@login_required
def faculty_courses_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    courses = Course.objects.all().order_by('title')
    return render(request, 'dashboard/faculty/courses_list.html', {'courses': courses})


@login_required
def faculty_course_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course created.')
            return redirect('dashboard:faculty_courses_list')
    else:
        form = CourseForm()
    return render(request, 'dashboard/faculty/course_form.html', {'form': form})


@login_required
def faculty_course_edit(request, slug):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated.')
            return redirect('dashboard:faculty_courses_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'dashboard/faculty/course_form.html', {'form': form, 'course': course})


@login_required
def faculty_course_materials(request, slug):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    course = get_object_or_404(Course, slug=slug)
    assignments = course.assignments.all()
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, 'Material/assignment uploaded.')
            return redirect('dashboard:faculty_course_materials', slug=slug)
    else:
        form = AssignmentForm()
    return render(request, 'dashboard/faculty/course_materials.html', {'course': course, 'assignments': assignments, 'form': form})


@login_required
def faculty_grade_submissions_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    submissions = Submission.objects.select_related('assignment', 'student').order_by('-submitted_at')
    return render(request, 'dashboard/faculty/grade_submissions_list.html', {'submissions': submissions})


@login_required
def faculty_grade_submission(request, submission_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    submission = get_object_or_404(Submission, pk=submission_id)
    try:
        grade = submission.grade
    except Grade.DoesNotExist:
        grade = None
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            g = form.save(commit=False)
            g.submission = submission
            g.save()
            messages.success(request, 'Grade saved.')
            return redirect('dashboard:faculty_grade_submissions_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'dashboard/faculty/grade_form.html', {'submission': submission, 'form': form})


@login_required
def faculty_staff_tasks(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    tasks = StaffTask.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = StaffTaskForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.created_by = request.user
            t.save()
            messages.success(request, 'Task created.')
            return redirect('dashboard:faculty_staff_tasks')
    else:
        form = StaffTaskForm()
    return render(request, 'dashboard/faculty/staff_tasks.html', {'tasks': tasks, 'form': form})


@login_required
def faculty_staff_notes(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    notes = StaffNote.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = StaffNoteForm(request.POST)
        if form.is_valid():
            n = form.save(commit=False)
            n.author = request.user
            n.save()
            messages.success(request, 'Note saved.')
            return redirect('dashboard:faculty_staff_notes')
    else:
        form = StaffNoteForm()
    return render(request, 'dashboard/faculty/staff_notes.html', {'notes': notes, 'form': form})

@login_required
def dashboard_index(request):
    # Route non-staff to the student dashboard
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard:student_index')

    # Simple dashboard context for now
    context = {
        'stats': {
            'news_count': 0,
            'events_count': 0,
            'messages_count': 0,
            'downloads_count': 0,
            'unread_messages': 0,
        },
        'recent_news': [],
        'recent_messages': [],
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def student_dashboard(request):
    # Basic student dashboard
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard/student/index.html', context)


@login_required
def student_courses(request):
    # Show courses the student is enrolled in and available courses
    enrolled = Course.objects.filter(enrollment__student=request.user)
    available = Course.objects.exclude(enrollment__student=request.user)
    return render(request, 'dashboard/student/courses.html', {'enrolled': enrolled, 'available': available})


@login_required
def student_course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    is_enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()
    assignments = course.assignments.all()

    # simple progress: number of submissions / number of assignments
    total = assignments.count()
    submitted = Submission.objects.filter(assignment__in=assignments, student=request.user).count()
    progress = int((submitted / total) * 100) if total > 0 else 0

    return render(request, 'dashboard/student/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'assignments': assignments,
        'progress': progress,
    })


@login_required
def student_join_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f'You have joined {course.title}.')
    return redirect(course.get_absolute_url())


@login_required
def student_leave_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    Enrollment.objects.filter(student=request.user, course=course).delete()
    messages.success(request, f'You have left {course.title}.')
    return redirect('dashboard:student_courses')


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = Submission.objects.filter(assignment=assignment, student=request.user)
    return render(request, 'dashboard/student/assignment_detail.html', {'assignment': assignment, 'submissions': submissions})


@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully.')
            return redirect('dashboard:student_assignments')
    else:
        form = SubmissionForm()
    return render(request, 'dashboard/student/submit_assignment.html', {'form': form, 'assignment': assignment})


@login_required
def student_assignments(request):
    assignments = []
    return render(request, 'dashboard/student/assignments.html', {'assignments': assignments})


@login_required
def student_grades(request):
    grades = []
    return render(request, 'dashboard/student/grades.html', {'grades': grades})


@login_required
def staff_dashboard(request):
    # Only allow staff or superusers
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    context = {}
    return render(request, 'dashboard/staff/index.html', context)


@login_required
def staff_student_management(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    students = []
    return render(request, 'dashboard/staff/student_management.html', {'students': students})


@login_required
def staff_students_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    students = User.objects.filter(is_staff=False).order_by('last_name', 'first_name')
    return render(request, 'dashboard/staff/students_list.html', {'students': students})


@login_required
def staff_edit_student(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    student = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student profile updated.')
            return redirect('dashboard:staff_students_list')
    else:
        form = StudentEditForm(instance=student)
    return render(request, 'dashboard/staff/edit_student.html', {'form': form, 'student': student})


@login_required
@require_http_methods(['POST'])
def staff_reset_password(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    student = get_object_or_404(User, pk=user_id)
    temp = User.objects.make_random_password()
    student.set_password(temp)
    student.save()
    messages.success(request, f"Password reset. Temporary password: {temp}")
    return redirect('dashboard:staff_edit_student', user_id=user_id)


@login_required
def staff_enroll_student(request, user_id, slug):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    student = get_object_or_404(User, pk=user_id)
    course = get_object_or_404(Course, slug=slug)
    Enrollment.objects.get_or_create(student=student, course=course)
    messages.success(request, f"{student.get_full_name() or student.username} enrolled in {course.title}.")
    return redirect('dashboard:staff_students_list')


@login_required
def staff_unenroll_student(request, user_id, slug):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    student = get_object_or_404(User, pk=user_id)
    course = get_object_or_404(Course, slug=slug)
    Enrollment.objects.filter(student=student, course=course).delete()
    messages.success(request, f"{student.get_full_name() or student.username} unenrolled from {course.title}.")
    return redirect('dashboard:staff_students_list')


@login_required
def staff_view_performance(request, user_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    student = get_object_or_404(User, pk=user_id)
    submissions = Submission.objects.filter(student=student).select_related('assignment')
    return render(request, 'dashboard/staff/student_performance.html', {'student': student, 'submissions': submissions})


@login_required
def staff_support_tools(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    tools = []
    return render(request, 'dashboard/staff/support_tools.html', {'tools': tools})


@login_required
def tickets_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    tickets = Ticket.objects.all().order_by('-created_at')
    return render(request, 'dashboard/staff/tickets_list.html', {'tickets': tickets})


@login_required
def ticket_detail(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket updated.')
            return redirect('dashboard:ticket_detail', pk=pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'dashboard/staff/ticket_detail.html', {'ticket': ticket, 'form': form})


@login_required
def announcements_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    items = Announcement.objects.all().order_by('-created_at')
    return render(request, 'dashboard/staff/announcements_list.html', {'items': items})


@login_required
def announcement_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.created_by = request.user
            ann.save()
            messages.success(request, 'Announcement published.')
            return redirect('dashboard:announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'dashboard/staff/announcement_form.html', {'form': form})


@login_required
def documents_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    docs = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/staff/documents_list.html', {'docs': docs})


@login_required
def document_upload(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            d = form.save(commit=False)
            d.uploaded_by = request.user
            d.save()
            messages.success(request, 'Document uploaded.')
            return redirect('dashboard:documents_list')
    else:
        form = DocumentUploadForm()
    return render(request, 'dashboard/staff/document_upload.html', {'form': form})


@login_required
def faculty_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    return render(request, 'dashboard/faculty/index.html', {})


@login_required
def faculty_course_builder(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    return render(request, 'dashboard/faculty/course_builder.html', {})


@login_required
def faculty_grade_submissions(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    return render(request, 'dashboard/faculty/grade_submissions.html', {})


@login_required
def faculty_staff_coordination(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard:index')
    return render(request, 'dashboard/faculty/staff_coordination.html', {})
