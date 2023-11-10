import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

"""
    The validators should return True if everything is working perfectly, or the error
    as string if there is a problem
"""

_name_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
_url_validation = URLValidator()

def name_validator(value):

    if not _name_pattern.match(value):
        return "invalid name"
    return True


def tag_validator(value):

    for x in value.split(','):
        if not re.match('^[a-zA-Z0-9_]+$', x.strip()):
            return "invalid tags"

    return True


def url_validator(value):

    try:
        _url_validation(value)
        return True
    
    except ValidationError:
        return "invalid url"