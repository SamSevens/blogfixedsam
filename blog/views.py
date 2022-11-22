# blog/views.py

from django.shortcuts import render
from . import models


def home(request):
    """
    The Blog homepage
    """
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.get_authors()
    topics = models.Topic.objects.all()[:10]
    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'topics': topics
    }

    return render(request, 'blog/home.html', context)
