from django.contrib import admin
from notification.models import Notification, NotifyComment

admin.site.register(Notification)
admin.site.register(NotifyComment)
