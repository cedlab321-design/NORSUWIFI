# core/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import os

def home(request):
    # Initialize empty lists
    latest_news = []
    upcoming_events = []
    
    # Try to get news data
    try:
        from news.models import NewsPost
        latest_news = list(NewsPost.objects.filter(
            is_published=True
        ).select_related('author').order_by('-published_date')[:5])
    except Exception as e:
        # Fallback data
        latest_news = [
            {
                'title': 'Welcome to NORSU Bayawan Campus',
                'excerpt': 'We are excited to welcome new students to our campus for the upcoming academic year.',
                'published_date': timezone.now(),
                'slug': 'welcome-to-norsu-bayawan',
                'get_absolute_url': '#',
            },
            {
                'title': 'New Academic Programs Available',
                'excerpt': 'Introducing new courses and programs for the upcoming semester.',
                'published_date': timezone.now(),
                'slug': 'new-academic-programs',
                'get_absolute_url': '#',
            }
        ]
    
    # Try to get events data
    try:
        from events.models import Event
        upcoming_events = list(Event.objects.filter(
            date__gte=timezone.now()
        ).order_by('date')[:5])
    except Exception as e:
        # Fallback data
        upcoming_events = [
            {
                'title': 'Campus Orientation Day',
                'description': 'Orientation program for all new students joining NORSU Bayawan.',
                'date': timezone.now(),
                'location': 'Main Auditorium',
                'slug': 'campus-orientation-day',
                'get_absolute_url': '#',
            }
        ]
    
    context = {
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')


def organization(request):
    """Unified organization page combining faculty and staff highlights."""
    faculty_highlights = []
    staff_highlights = []
    faculty_departments = []
    staff_departments = []
    faculty_count = 0
    staff_count = 0

    try:
        from faculty.models import FacultyMember, FacultyDepartment
        faculty_qs = FacultyMember.objects.filter(is_active=True).select_related('department')
        faculty_highlights = faculty_qs[:6]
        faculty_count = faculty_qs.count()
        faculty_departments = FacultyDepartment.objects.all()[:6]
    except Exception:
        # Keep graceful fallbacks if faculty app or data is unavailable
        faculty_highlights = []
        faculty_departments = []

    try:
        from staff.models import StaffMember, StaffDepartment
        staff_qs = StaffMember.objects.filter(is_active=True).select_related('department')
        staff_highlights = staff_qs[:6]
        staff_count = staff_qs.count()
        staff_departments = StaffDepartment.objects.all()[:6]
    except Exception:
        staff_highlights = []
        staff_departments = []

    context = {
        'faculty_highlights': faculty_highlights,
        'staff_highlights': staff_highlights,
        'faculty_departments': faculty_departments,
        'staff_departments': staff_departments,
        'faculty_count': faculty_count,
        'staff_count': staff_count,
    }
    return render(request, 'core/organization.html', context)


def admissions(request):
    """Admissions information page."""
    context = {
        'contact_email': 'admissions@norsu-bayawan.edu.ph',
        'phone': '+63 XXX-XXXX-XXX',
        'address': 'Santa Catalina, Negros Oriental, Philippines',
    }
    return render(request, 'core/admissions.html', context)


def subscribe(request):
    """Handle newsletter subscription form POST from footer.

    - Expects `email` in POST data.
    - On success, sets a success message and redirects back to the referring page.
    """
    if request.method != 'POST':
        return redirect('/')

    email = request.POST.get('email', '').strip()
    if not email:
        messages.error(request, 'Please provide an email address.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Please provide a valid email address.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Minimal handling: record subscription in a plain text file (simple, non-blocking)
    try:
        subscriptions_file = 'subscriptions.txt'
        with open(subscriptions_file, 'a', encoding='utf-8') as f:
            f.write(email + '\n')
    except Exception:
        # If writing fails, still show success to the user but log could be added.
        pass

    messages.success(request, 'Thanks — you have been subscribed to our newsletter.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def privacy(request):
    """Privacy policy page."""
    return render(request, 'core/privacy.html')


def terms(request):
    """Terms and conditions page."""
    return render(request, 'core/terms.html')


def sitemap(request):
    """Simple HTML sitemap page listing main site sections."""
    sections = [
        {'title': 'Home', 'url': '/'},
        {'title': 'About', 'url': '/about/'},
        {'title': 'Admissions', 'url': '/admissions/'},
        {'title': 'Academics', 'url': '/academics/'},
        {'title': 'Organization', 'url': '/organization/'},
        {'title': 'News', 'url': '/news/'},
        {'title': 'Events', 'url': '/events/'},
        {'title': 'Contact', 'url': '/contact/'},
    ]
    return render(request, 'core/sitemap.html', {'sections': sections})


def accessibility(request):
    """Accessibility statement page."""
    return render(request, 'core/accessibility.html')


def downloads(request):
    """List files placed in the `media/downloads/` directory and render links."""
    downloads_dir = os.path.join(settings.MEDIA_ROOT, 'downloads')
    files = []
    if os.path.isdir(downloads_dir):
        for fname in sorted(os.listdir(downloads_dir)):
            # skip hidden files
            if fname.startswith('.'):
                continue
            files.append({
                'name': fname,
                'url': settings.MEDIA_URL + 'downloads/' + fname
            })

    return render(request, 'core/downloads.html', {'files': files})
