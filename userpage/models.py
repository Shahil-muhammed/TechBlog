import uuid
from django.db import models
from accounts.models import CustomUser
from urllib.parse import urlparse, parse_qs
from ckeditor_uploader.fields import RichTextUploadingField

class Blog(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # Rich content with text + media support
    youtube_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated search keywords"
    )

    # SEO fields
    seo_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Recommended: Max 60 characters"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Recommended: Max 160 characters for SEO"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def get_youtube_embed_id(self):
        """
        Extracts the YouTube video ID from the youtube_link.
        Supports both youtu.be and youtube.com URLs.
        """
        if not self.youtube_link:
            return None

        url = urlparse(self.youtube_link)

        if 'youtu.be' in url.netloc:
            return url.path.lstrip('/')

        if 'youtube.com' in url.netloc:
            query = parse_qs(url.query)
            return query.get('v', [None])[0]

        return None

    def __str__(self):
        return self.title


    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'
