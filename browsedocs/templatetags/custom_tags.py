import os
import json
import pytz
from urllib.parse import urlparse
from datetime import datetime, timezone

from django import template
from django.utils import timezone
from django.core import exceptions

from delta import html

register = template.Library()


@register.filter
def filename(value):
    """
        returns just the file name
    """
    return os.path.basename(value.name)

@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def utc_to_local(utc_datetime, user_timezone, date_format="%b. %d, %Y, %I:%M %p"):
    
    if utc_datetime and user_timezone:
        if not isinstance(utc_datetime, str):
            utc_datetime = str(utc_datetime)

        try:
            user_timezone = pytz.timezone(user_timezone)  

        except pytz.UnknownTimeZoneError:
            pass

        utc_datetime_obj = datetime.fromisoformat(utc_datetime)
        utc_datetime_obj = utc_datetime_obj.replace(tzinfo=pytz.UTC)
        
        specific_datetime = utc_datetime_obj.astimezone(user_timezone)
        # print("date: ", specific_datetime, specific_datetime.strftime(date_format), date_format)
        return specific_datetime.strftime(date_format)
    
    else:
        return utc_datetime.strftime(date_format)

@register.filter
def get_key(items: dict, index=0):
    return list(items.keys())[index]

@register.filter
def get_value(items: dict, index=0):
    return list(items.values())[index]


@register.filter
def extract_path(url):
    """
        extracts path from url
    """
    path = urlparse(url).path
    return path[1:]


@register.filter
def render_delta(delta: dict):
    """
        extracts path from url
    """
    return html.render(json.loads(delta)['ops'])
