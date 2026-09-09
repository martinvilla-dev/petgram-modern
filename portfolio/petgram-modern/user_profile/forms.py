from django import forms
from .models import CustomUser

class  ProfileForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ("profile_pic", "display_name", "bio", "website", "pet_type")
        widgets = {
            'display_name': forms.TextInput(attrs={"class":"form-control post-form"}),
            'bio': forms.Textarea(attrs={"class":"form-control post-form"}),
            'website': forms.TextInput(attrs={"class":"form-control post-form"}),
            'pet_type': forms.Select(attrs={"class":"form-control post-form"}),
        }
