# blogfixedsam/views.py

from django.shortcuts import render


def home(request):
    """
    The Blog homepage
    """
    return render(request, 'blog/base.html')
