from django.db import models
from django.utils import timezone
from user_profile.models import CustomUser
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    display_name = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    post_file= models.FileField(upload_to='post/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'heic', 'HEIC', 'mp4', 'mov', 'png'])], null=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    user_likes = models.ManyToManyField(CustomUser, related_name='user_likes', symmetrical=False, default=CustomUser, blank=True)
    dislikes = models.IntegerField(default=0)
    
    # NEW fields for geo-location and filters
    location = models.CharField(max_length=255, blank=True, null=True)
    filter_style = models.CharField(max_length=50, blank=True, null=True, default='normal')

    @property
    def is_video(self):
        if self.post_file and self.post_file.url:
            url_lower = self.post_file.url.lower()
            return url_lower.endswith('.mp4') or url_lower.endswith('.mov')
        return False

    def __str__(self):
        return f'{self.display_name} | {self.caption}'

class Comment(models.Model):
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, related_name='commenter', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Hashtags(models.Model):
    post = models.ManyToManyField(Post)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.slug