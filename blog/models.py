from django.db import models

from django_quill.fields import QuillField

from user.models import User

from docsapp.models import Project

from utils.constraint_fields import ContentTypeRestrictedFileField


class Blog(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    body = QuillField(null=True, blank=True)
    tag = models.CharField(max_length=150, null=True, blank=True)

    datetime = models.DateTimeField(auto_now=True)

    draft = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BlogImage(models.Model):

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image =  ContentTypeRestrictedFileField(upload_to='blog-media/', null=True, blank=True, 
                                            max_upload_size=5242880, content_types=["image/jpeg", "image/png", "image/jpg", "image/gif"])

    def __str__(self):
        return self.blog.title[:30]
