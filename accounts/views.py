# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from .forms_settings import SettingsForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('/dashboard/')  # Absolute path
            return redirect('/')  # Absolute path
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def register_view(request):
    """Simple registration view that creates a `User` and default `UserProfile`.
    On success the new user is logged in and redirected to their profile.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        id_number = request.POST.get('id_number', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not password1 or not id_number:
            messages.error(request, 'Username, ID Number, and password are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            # automatically created UserProfile by signal in models.py
            profile = getattr(user, 'userprofile', None)
            if profile:
                profile.id_number = id_number
                profile.save()
            login(request, user)
            messages.success(request, 'Account created and logged in.')
            return redirect('accounts:profile')

    return render(request, 'accounts/register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')  # Absolute path

@login_required
def dashboard_index(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')  # Absolute path
    
    context = {
        'stats': {
            'news_count': 0,
            'events_count': 0,
            'messages_count': 0,
            'downloads_count': 0,
            'unread_messages': 0,
        },
        'recent_news': [],
        'recent_messages': [],
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def profile(request):
    """Simple profile view — displays basic user info."""
    user = request.user

    # Ensure user has a profile (signal creates on user creation)
    profile = getattr(user, 'userprofile', None)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'user_obj': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def settings_view(request):
    """Simple account settings view. Offers links to change profile/password and preferences."""
    user = request.user

    if request.method == 'POST':
        form = SettingsForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated.')
            return redirect('accounts:settings')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = SettingsForm(user=user)

    context = {
        'user_obj': user,
        'form': form,
    }
    return render(request, 'accounts/settings.html', context)
