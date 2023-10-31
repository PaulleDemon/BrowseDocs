from django.db import models

from utils.constraint_fields import ContentTypeRestrictedFileField


class DocType(models.Model):

    """
        specifies the type of the documentation eg: Language or Tool etc
    """

    name = models.CharField(max_length=50)
    icon = ContentTypeRestrictedFileField(upload_to='blog-media/', null=True, blank=True, 
                                            max_upload_size=5242880, content_types=["image/jpeg", "image/png", "image/jpg"])
    

class DocSubType(models.Model):

    """
        This is where we specify the name of the language or the tool. 
        the shortened_name referes to the shortned form  eg: python -> py
    """

    doctype = models.ForeignKey(DocType, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    shortened_name = models.CharField(max_length=10)

