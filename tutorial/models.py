from django.db import models

from user.models import User

from utils.constraint_fields import ContentTypeRestrictedFileField


class Tutorial(models):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    project = models.ForeignKey(null=True, blank=True)

    text = models.TextField()
    tag = models.CharField(max_length=100)

    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TutorialImage(models):

    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    image =  ContentTypeRestrictedFileField(upload_to='tutorial-media/', null=True, blank=True, 
                                            max_upload_size=5242880, content_types=["image/jpeg", "image/png", "image/jpg", "image/gif"])

    def __str__(self):
        return self.tutorial.title[:30]
