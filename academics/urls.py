# academics/urls.py
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.department_list, name='index'),
    path('departments/', views.department_list, name='departments'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
]