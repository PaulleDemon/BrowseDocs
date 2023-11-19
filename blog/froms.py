from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'body', 'draft', 'project', 'published', 'tag']