from celery import shared_task
from celery.utils.log import get_task_logger

from django.urls import reverse
from django.core.mail import send_mass_mail, send_mail

from .common import get_name_from_email
from .mailing import send_mass_html_mail
from .doc_generator import generate_docs

from user.models import User

logger = get_task_logger(__name__)


@shared_task
def send_html_mail_celery(subject, message, html_message, from_email=None, recipient_list=[]):
    send_mass_html_mail(subject, message, html_message, from_email, recipient_list)


@shared_task
def send_mass_mail_celery(subject, message, from_email=None, recipient_list=[]):
    send_mass_mail([(subject, message, from_email, recipient_list)])


@shared_task
def send_mail_celery(subject, message, from_email=None, recipient_list=[]):

    send_mail(subject, message, from_email=from_email, recipient_list=recipient_list)


@shared_task
def generate_docs_celery(user_id, project_id: int):
    
    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return 

    generated = generate_docs(user, project_id)

    if generated != True:

        message = f"Hi {get_name_from_email(user.email)},\n Your documentation creation failed due to the following reasons: {' '.join([x for x in generated])}.\n\n Please go to dashboard and try again after rectifying errors.\n\n Best regards,\nBrowseDocs Team"

        send_mail_celery.delay("Docs creation failed", message, recipient_list=[user.email])

    else:
        print("successful")
        message = f"Hi {get_name_from_email(user.email)},\n Your documentation creation was successful. Please visit the following to .\n\n Best regards,\nBrowseDocs Team"

        send_mail_celery.delay("Docs creation Successful", message, recipient_list=[user.email])