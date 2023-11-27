from typing import Any
from django import forms
from django.core.exceptions import ValidationError

from .models import (Project, AdditionalLink, Sponsor, Social, 
                        Documentation, DocPage)


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ('datetime', 'user', 'unique_id')

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk and cleaned_data.get('unique_name') != self.instance.unique_name:  # If the instance is being created for the first time
            raise ValidationError({"unique_name": "Unique name cannot be updated"})

        if len(cleaned_data.get('name')) < 3:
            raise ValidationError({"name": "Name must be atleast 3 characters long"})

        return cleaned_data
    

class DocumentationForm(forms.ModelForm):

    class Meta:
        model = Documentation
        exclude = ('datetime', 'last_updated')


class DocPageForm(forms.ModelForm):

    class Meta:
        model = DocPage
        exclude = ('datetime', 'last_updated')

class LinkForm(forms.ModelForm):

    class Meta:
        model = AdditionalLink
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if AdditionalLink.objects.filter(project=cleaned_data.get('project')).count() >= 2:
            raise ValidationError({"link": "Only 2 additional links can be added at this time"})

        return cleaned_data


class SocialForm(forms.ModelForm):


    class Meta:
        model = Social
        fields = '__all__'


class SponsorForm(forms.ModelForm):

    class Meta:
        model = Sponsor
        fields = '__all__'