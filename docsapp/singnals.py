from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete

from utils.tasks import generate_docs_celery

from urllib.parse import urlparse
from .models import Project, DocPage, Documentation


@receiver(post_save, sender=Project)
def update_documentation(instance, sender, created, *args, **kwargs):
    
    generate_docs_celery.delay(user_id=instance.user.id, project_id=instance.id)