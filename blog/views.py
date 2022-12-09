# blog/views.py
from django.db.models import Count
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from . import models
from . import forms, models
from django.views.generic import DetailView, FormView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, CreateView, FormView, ListView


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        # Update the context with our context variables
        context.update({
            'latest_posts': latest_posts

        })

        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'


def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')


class TopicDetailView(DetailView):
    model = models.Topic

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     queryset = models.Post.objects.all().published().filter(
    #         topics__slug=self.kwargs['slug']
    #     )
    #     context['posts'] = queryset


class TopicListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Topic.objects.all().annotate(c=Count('blog_posts')).order_by('name')


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )


class ContestFormView(FormView):
    template_name = 'blog/upload_form.html'
    form_class = forms.ContestForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Create a "success" message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for submitting your photo!'
        )
        form.save()
        return super().form_valid(form)


def form_example(request):
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template.
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
    # If not a POST, return a blank form
    else:
        form = forms.ExampleSignupForm()

    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})


class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)
