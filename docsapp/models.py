from django.db import models

from user.models import User

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


class Project(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=100)
    unique_name = models.CharField(max_length=40, unique=True, validators=[name_validator])
    version = models.CharField(max_length=10)
    about = models.TextField(max_length=500)

    project_logo = models.URLField(null=True, blank=True)

    source = models.URLField()
    source_code = models.URLField(null=True, blank=True)

    doc_type = models.PositiveSmallIntegerField(choices=DOC_TYPE.choices, default=DOC_TYPE.PROGRAMMING_LANG)
    # source = models.

    datetime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

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

    