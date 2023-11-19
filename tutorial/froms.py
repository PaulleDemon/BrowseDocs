from django import forms
from .models import Tutorial


class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['id', 'title', 'body', 'draft', 'project', 'published', 'tag']