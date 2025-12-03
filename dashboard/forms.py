from django import forms
from .models import Submission, Ticket, Announcement, Document
from django.contrib.auth import get_user_model


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded border p-2'}),
        }


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status']


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body', 'publish']


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']


# Bind the models defined in models.py to the generic form placeholders
from .models import Course, Assignment, Grade, StaffTask, StaffNote


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'outline', 'schedule']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'attachment']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['value', 'feedback']


class StaffTaskForm(forms.ModelForm):
    class Meta:
        model = StaffTask
        fields = ['title', 'description', 'assigned_to', 'due_date', 'completed']


class StaffNoteForm(forms.ModelForm):
    class Meta:
        model = StaffNote
        fields = ['title', 'body']


class CourseForm(forms.ModelForm):
    class Meta:
        model = None
        # imported dynamically below


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = None
        # filled in below


class GradeForm(forms.ModelForm):
    class Meta:
        model = None
        # filled in below


class StaffTaskForm(forms.ModelForm):
    class Meta:
        model = None
        # filled in below


class StaffNoteForm(forms.ModelForm):
    class Meta:
        model = None
        # filled in below

