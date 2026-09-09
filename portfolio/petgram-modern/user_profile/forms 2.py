from django import forms
from .models import CustomUser

class  ProfileForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ("profile_pic", "display_name", "bio", "website", "pet_type")
