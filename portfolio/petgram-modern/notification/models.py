from django.db import models
from django.utils import timezone
from user_profile.models import CustomUser
from post.models import Post, Comment

class Notification(models.Model):
    reciever = models.ForeignKey(CustomUser, related_name='reciever', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    text = models.ForeignKey(Post, related_name='post_notify', on_delete=models.CASCADE)

    def __str__(self):
        return self.text.caption

class NotifyComment(models.Model):
    reciever = models.ForeignKey(CustomUser, related_name='recieving', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    text = models.ForeignKey(Comment, related_name='comment_notify', on_delete=models.CASCADE)

    def __str__(self):
        return self.text.comment

