
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


def get_file_name(file_path: str):
    """
        given a string path returns the file name
    """

    name = file_path.split("/")

    return name[0].split(".")[0]



def extract_path(path: str):
    """
    Given path returns a proper path, e.g., /docs#heading1 -> docs/
    """

    path_parts = path.split("#", 1)
    path_parts = path_parts[0].split("?", 1)

    path_components = path_parts[0].split("/")
    path_components = [component for component in path_components if component]

    result_path = '/'.join(path_components)

    if not path.endswith('/'):
        result_path += '/'

    return result_path