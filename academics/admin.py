# academics/admin.py
from django.contrib import admin
from .models import Department, Course

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'email', 'created_at')
    search_fields = ('name', 'head', 'description')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'department', 'duration')
    list_filter = ('department',)
    search_fields = ('title', 'code', 'description')