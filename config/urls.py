"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# config/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from accounts import views as accounts_views
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # This should be here
    path('accounts/', include('accounts.urls')),
    path('profile/', accounts_views.profile, name='profile'),
    path('settings/', accounts_views.settings_view, name='settings'),
    path('academics/', include('academics.urls')),
    path('news/', include('news.urls')),
    path('events/', include('events.urls')),
    path('contact/', include('contact.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('subscribe/', core_views.subscribe, name='subscribe'),
    re_path(r'^faculty/.*$', RedirectView.as_view(pattern_name='core:organization', permanent=False)),
    re_path(r'^staff/.*$', RedirectView.as_view(pattern_name='core:organization', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
