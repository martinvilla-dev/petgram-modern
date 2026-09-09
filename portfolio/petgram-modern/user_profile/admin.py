from django.contrib import admin
from user_profile.models import CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(CustomUser)