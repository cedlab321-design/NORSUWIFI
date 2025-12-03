# news/admin.py
from django.contrib import admin
from .models import NewsPost  # Updated import

@admin.register(NewsPost)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published_date', 'is_published', 'is_featured']
    list_filter = ['category', 'is_published', 'is_featured', 'published_date']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'image')
        }),
        ('Classification', {
            'fields': ('category', 'is_featured')
        }),
        ('Publication', {
            'fields': ('author', 'published_date', 'is_published')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)