# events/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event

def event_list(request):
    try:
        upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
        
        context = {
            'upcoming_events': upcoming_events,
            'past_events': past_events,
        }
    except Exception as e:
        # Fallback if there's any issue
        context = {
            'upcoming_events': [],
            'past_events': [],
        }
    
    return render(request, 'events/event_list.html', context)

def event_detail(request, slug):
    try:
        event = get_object_or_404(Event, slug=slug)
        context = {
            'event': event,
        }
    except:
        # Fallback if event not found
        context = {
            'event': None,
        }
    
    return render(request, 'events/event_detail.html', context)