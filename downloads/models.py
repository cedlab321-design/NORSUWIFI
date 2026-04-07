from django.db import models

class DownloadFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='downloads/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Download File"
        verbose_name_plural = "Download Files"