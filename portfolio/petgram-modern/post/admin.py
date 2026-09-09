from django.contrib import admin
from post.models import Post, Comment, Hashtags

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(Hashtags)
