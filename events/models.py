# events/models.py
from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Events"
        ordering = ['-date']
    
    def __str__(self):
        return self.title