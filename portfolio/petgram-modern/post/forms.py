from django import forms
from django.forms import ModelForm
from post.models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('post_file', 'caption', 'location', 'filter_style')
        widgets = {
            'caption': forms.Textarea(attrs={"class":"form-control post-form", "rows": 3}),
            'location': forms.TextInput(attrs={"class":"form-control", "placeholder": "Add location (e.g., Orange, CA)"}),
            'filter_style': forms.Select(attrs={"class":"form-control"}, choices=[
                ('normal', 'Normal'),
                ('grayscale', 'Black & White'),
                ('sepia', 'Sepia'),
                ('vintage', 'Vintage'),
            ]),
        }
    
class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))