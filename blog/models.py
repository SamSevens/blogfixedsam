from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class TopicQuerySet(models.QuerySet):
    def get_topics(self):
        return self.model.name


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        User = get_user_model()
        # Get the users who are authors of this queryset
        return User.objects.filter(blog_posts__in=self).distinct()


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/topics/" + self.slug

    class Meta:
        ordering = ['name']

    objects = TopicQuerySet.as_manager()


class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255)
    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )

    slug = models.SlugField(
        null=False,
        unique_for_date='published',  # Slug is unique for publication date
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )

    content = RichTextUploadingField()

    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )

    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()  # The current datetime with timezone

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)


class Comment(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, null=False)
    post = models.ForeignKey(Post, related_name='comments', null=False, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    APPROVED = 'approved'
    REJECTED = 'rejected'
    APPROVED_CHOICES = [
        (APPROVED, 'approved'),
        (REJECTED, 'rejected')
    ]

    approved = models.CharField(
        max_length=10,
        choices=APPROVED_CHOICES,
        default=REJECTED,
        help_text='Set to "approved" to make this post publicly visible',
        )

    created = models.DateTimeField(auto_now=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Comment by {}'.format(self.name)


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'


class Contest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    photo = models.ImageField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']
        verbose_name = "Photo contest submissions"

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'
