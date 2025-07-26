from django.contrib import admin
from .models import Blog, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'keywords', 'seo_title', 'meta_description')
    list_filter = ('created_at',)
    readonly_fields = ('uid', 'created_at')
    autocomplete_fields = ['author']
    fields = (
        'uid',
        'title',
        'seo_title',
        'meta_description',
        'content',
        'image',
        'youtube_link',
        'author',
        'keywords',
        'created_at',
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)
    autocomplete_fields = ['blog', 'user']
