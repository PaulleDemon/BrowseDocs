from django.db import models

from django_quill.fields import QuillField

from user.models import User

from utils.common import generate_uniqueid
from utils.validators import name_validator, tag_validator
from utils.constraint_fields import ContentTypeRestrictedFileField


class SOCIAL(models.IntegerChoices):

    REDDIT = (0, 'Reddit')
    TWITTER = (1, 'Twitter')
    DISCORD = (2, 'Discord')
    MASTODON = (3, 'Mastodon')
    STACKOVERFLOW = (4, 'Stackoverflow')


class DOC_TYPE(models.IntegerChoices):

    PROGRAMMING_LANG = (0, 'pgm-lang')
    TOOL = (1, 'tool')


class SPONSORS(models.IntegerChoices):

    OPEN_COLLECTIVE = (0, 'Open collective')
    GITHUB = (1, 'Github')
    BUYMEACOFFEE = (2, 'Buy me a coffee')
    PATREON = (3, 'Patreon')
    PAYPAL = (4, 'Paypal')


class LANG(models.IntegerChoices):

    EN = (0, 'English')
    FR = (1, 'French')
    DE = (2, 'German')
    RU = (3, 'Russian')


def generate_id():
    return generate_uniqueid(Project, 'unique_id')

class Project(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=100)

    unique_id = models.CharField(max_length=20, unique=True, default=generate_id)

    unique_name = models.CharField(max_length=40, unique=True, validators=[name_validator])
    version = models.CharField(max_length=10)
    about = models.TextField(max_length=500)

    project_logo = models.URLField(null=True, blank=True)

    source = models.URLField()
    source_code = models.URLField(null=True, blank=True)

    authors = models.TextField(max_length=2000, null=True, blank=True)

    doc_type = models.PositiveSmallIntegerField(choices=DOC_TYPE.choices, default=DOC_TYPE.PROGRAMMING_LANG)
    # source = models.

    datetime = models.DateTimeField(auto_now_add=True)

    doc_path = models.CharField(max_length=250, null=True, blank=True) # the source in the config file, ie the path
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.unique_name = self.unique_name.lower()
        return super().save(*args, **kwargs)


class Social(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name = models.PositiveSmallIntegerField(choices=SOCIAL.choices, default=SOCIAL.STACKOVERFLOW)
    username = models.CharField(max_length=45, validators=[name_validator])


class Sponsor(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name = models.PositiveSmallIntegerField(choices=SPONSORS.choices, default=SPONSORS.GITHUB)
    username = models.CharField(max_length=45, validators=[name_validator])


class AdditionalLink(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    url = models.URLField()


class Documentation(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    version = models.CharField(max_length=10)
    lang = models.PositiveSmallIntegerField(choices=LANG.choices, default=LANG.EN)

    datetime = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    sidebar = models.JSONField(null=True, blank=True)


class DocPage(models.Model):

    name = models.CharField(max_length=80)
    page_url = models.CharField(max_length=250)

    documentation = models.ForeignKey(Documentation, on_delete=models.CASCADE)
    body = QuillField(null=True, blank=True)

    datetime = models.DateTimeField(auto_now_add=True)

    views = models.BigIntegerField(default=0)