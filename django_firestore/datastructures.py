# contains datastructures 
from typing import List, Dict, Union, TypedDict, Any
from .validators import tag_validator, name_validator, url_validator


class FieldValue(TypedDict):
    type: str
    minlength: int
    maxlength: int
    required: bool
    validators: List
    inner:  Union[Dict, List]

DatastructureType = Dict[str, FieldValue]


CREATE_PROJECT: DatastructureType = {
        'project_name': {'type': str, 'maxlength': 30, 'required': True},
        'unique_name': {'type': str, 'maxlength': 30, 'required': True},
        'version': {'type': str, 'maxlength': 10, 'required': True},
        'about': {'type': str, 'maxlength': 100, 'required': True},
        'project_logo': {'type': str, 'maxlength': 250, 'required': False, 'validators': [url_validator]},
        'tags': {'type': List[str], 'maxlength': 3, 'required': True, 'validators': [tag_validator]},
        'doc_type': {'type': str, 'maxlength': 10, 'required': True, 'validators': []},
        'social': {
            'inner':{
                'reddit': {'type': str, 'maxlength':30, 'required': False, 'validators': [name_validator]},
                'stackoverflow': {'type': str, 'maxlength':30, 'required': False, 'validators': [name_validator]},
                'twitter': {'type': str, 'maxlength':30, 'required': False, 'validators': [name_validator]},
                'mastodon': {'type': str, 'maxlength':30, 'required': False, 'validators': [name_validator]},
                'discord': {'type': str, 'maxlength':30, 'required': False, 'validators': [name_validator]},
            }
        },
        'additional_links': {
            'type': List[Dict],
            'minlength': 0,
            'maxlength': 2,
            'required': False,
            'repeat': True, # set this if the inner has to repeat
            'inner': [
                {
                    'link_name': {'type': str, 'maxlength': 20, 'required': True},
                    'link_url': {'type': str, 'required': True, 'validators': [url_validator]}
                }
            ]
            
        },
        'source': {'type': str, 'required': True, 'validators': [url_validator]},
        'source_code': {'type': str, 'required': False, 'validators': [url_validator]},
        'sponsor': {
            'inner': {
                'opencollective': {'type': str, 'maxlength': 25, 'required': False, 'validators': [name_validator]},
                'github': {'type': str, 'maxlength': 25, 'required': False, 'validators': [name_validator]},
                'buymeacoffee': {'type': str, 'maxlength': 25, 'required': False, 'validators': [name_validator]},
                'patreon': {'type': str, 'maxlength': 25, 'required': False, 'validators': [name_validator]},
            }   
        }
    }
