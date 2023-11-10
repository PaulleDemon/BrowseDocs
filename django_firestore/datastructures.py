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
        'name': {'type': str, 'maxlength': 30, 'required': True},
        'unique_name': {'type': str, 'maxlength': 30, 'required': True},
        'version': {'type': str, 'maxlength': 10, 'required': True},
        'about': {'type': str, 'maxlength': 100, 'required': True},
        'tags': {'type': List[str], 'maxlength': 3, 'required': True, 'validators': [tag_validator]},
        'doc_type': {'type': str, 'maxlength': 10, 'required': True, 'validators': []},
        'social': {
            'inner':{
                'reddit': {'type': str, 'maxlength':10, 'required': False, 'validators': [name_validator]},
                'stackoverflow': {'type': str, 'maxlength':10, 'required': False, 'validators': [name_validator]},
                'twitter': {'type': str, 'maxlength':10, 'required': False, 'validators': [name_validator]},
                'mastodon': {'type': str, 'maxlength':10, 'required': False, 'validators': [name_validator]},
                'discord': {'type': str, 'maxlength':10, 'required': False, 'validators': [name_validator]},
            }
        },
        'additional_links': {
            'type': List[Dict],
            'minlength': 0,
            'maxlength': 2,
            'inner': [
                {
                    'link_name': {'type': str, 'maxlength': 10, 'required': True, 'validators': [name_validator]},
                    'link_url': {'type': str, 'required': True, 'validators': [url_validator]}
                }
            ]
            
        },
        'source': {'type': str, 'required': True, 'validators': [url_validator]},
        'source_code': {'type': str, 'required': False, 'validators': [url_validator]},
        'sponsors': {
            'inner': {
                'opencollective': {'type': str, 'required': False, 'validators': [url_validator]},
                'github': {'type': str, 'required': False, 'validators': [url_validator]},
                'buymeacoffee': {'type': str, 'required': False, 'validators': [url_validator]},
                'patreon': {'type': str, 'required': False, 'validators': [url_validator]},
            }   
        }
    }
