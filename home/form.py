# posts/forms.py
from django import forms
from .models import Post, Comment

# Form for creating posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

# Form for adding comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
