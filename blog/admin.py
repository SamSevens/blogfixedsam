from django.contrib import admin
from . import models


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'created', 'updated', 'approved')
    list_filter = ('approved',)
    search_fields = ('name', 'email', 'text')


class CommentInline(admin.StackedInline):
    model = models.Comment
    readonly_fields = ('name', 'text', 'email',)
    can_delete = False
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'created',
        'updated',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )

    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        CommentInline,
    ]


admin.site.register(models.Post, PostAdmin)
