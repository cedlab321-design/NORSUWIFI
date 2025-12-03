# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import NewsPost

def news_list(request):
    try:
        news_list = NewsPost.objects.filter(is_published=True).order_by('-published_date')
        paginator = Paginator(news_list, 9)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'news_posts': page_obj,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
        }
    except Exception as e:
        # Fallback if there's any issue
        context = {
            'news_posts': [],
            'page_obj': None,
            'is_paginated': False,
        }
    
    return render(request, 'news/news_list.html', context)

def news_detail(request, slug):
    try:
        news = get_object_or_404(NewsPost, slug=slug, is_published=True)
        # Template expects `news_post` variable name; provide both for compatibility
        context = {
            'news': news,
            'news_post': news,
        }
    except Exception:
        # Fallback if news not found
        context = {
            'news': None,
            'news_post': None,
        }
    
    return render(request, 'news/news_detail.html', context)