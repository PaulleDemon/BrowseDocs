
from django.db import models
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile
"""
resused functionss
"""

def get_name_from_email(email):
    name, domain = email.split('@')
    return name.replace('.', ' ').strip().capitalize()


def get_file_size(request_file: UploadedFile, unit: str='MB'):
    """
    Get the file size from a file uploaded via request.FILES and convert it to KB or MB.

    """
    if unit not in ('KB', 'MB'):
        raise ValueError("Invalid unit. Please use 'KB' or 'MB'.")

    file_size_bytes = request_file.size

    if unit == 'MB':
        file_size = file_size_bytes / (1024 * 1024)  # 1 MB = 1024 KB
    else:
        file_size = file_size_bytes / 1024  # 1 KB = 1024 bytes

    return file_size


def generate_uniqueid(table: models.Model, field: str, length=12):

    unique_id = get_random_string(length=length)    

    # while table.objects.filter(**{field: unique_id}).exists():
    #     unique_id = get_random_string(length=length)    

    return unique_id
