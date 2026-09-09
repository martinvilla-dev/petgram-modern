from django.shortcuts import render
from notification.models import Notification, NotifyComment
from post.models import Post
from user_profile.models import CustomUser
from django.contrib.auth.decorators import login_required

def error_404_view(request,):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)

@login_required
def notification_view(request):
    user = request.user
    notifications = Notification.objects.filter(reciever=user, read=False)
    for alert in notifications:
        alert.read = True
        alert.save()
    comment_notify = NotifyComment.objects.filter(reciever=user, read=False)
    for notify in comment_notify:
        notify.read = True
        notify.save()
    return render(request, 'notification.html', {'notifications': notifications, 'comment_notify': comment_notify})

