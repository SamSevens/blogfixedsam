# blog/context_processors.py

from . import models


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    return {'authors': authors}
