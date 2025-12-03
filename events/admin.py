# events/admin.py
from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location']
    list_filter = ['date', 'location']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'content', 'image')
        }),
        ('Details', {
            'fields': ('date', 'location')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )