# blog/views.py

from django.shortcuts import render
from django.db.models import Count
from django.views import View
from . import models


def home(request):
    """
    The Blog homepage
    """
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.get_authors()
    topics = models.Topic.objects.all().annotate(c=Count('blog_posts')).order_by('-c')[:10]
    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'topics': topics
    }

    return render(request, 'blog/home.html', context)


class AboutView(View):
    def get(self, request):
        return render(request, 'blog/about.html')
