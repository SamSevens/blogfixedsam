# blog/context_processors.py
from django.db.models import Count
from . import models


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')
    topics = models.Topic.objects.all().annotate(c=Count('blog_posts')).order_by('-c')[:10]
    return {'authors': authors, 'topics': topics}
