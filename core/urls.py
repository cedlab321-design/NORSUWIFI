# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('organization/', views.organization, name='organization'),
    path('admissions/', views.admissions, name='admissions'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('accessibility/', views.accessibility, name='accessibility'),
    path('downloads/', views.downloads, name='downloads'),
]
