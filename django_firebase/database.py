import re
from typing import Any
from django.conf import settings

from google.cloud.firestore_v1 import Client
from google.cloud.firestore_v1.query import Query
from google.cloud.firestore_v1.base_query import FieldFilter

db_client: Client  = settings.FIRESTORE_CLIENT


class AbstractModel:

    def create_or_update(data: dict, pk=None):

        pass


class ValidationException(Exception):
    pass



def tag_validator(self, value):

    for x in value.split(','):
        if not re.match('^[a-zA-Z0-9_]+$', x.strip()):
            return "invalid tags"

    return True


def validate_data(data_structure, actual_data):
    errors = []
    validated_data = {}

    for key, rules in data_structure.items():
        if key not in actual_data:
            if rules.get('required', False):
                errors.append(f"'{key}' is required but not provided.")
            continue

        value = actual_data[key]

        if 'type' in rules and not isinstance(value, rules['type']):
            errors.append(f"'{key}' should be of type {rules['type']}.")

        if 'maxlength' in rules and len(value) > rules['maxlength']:
            errors.append(f"'{key}' exceeds the maximum length of {rules['maxlength']} characters.")

        if 'validators' in rules:
            for validator in rules['validators']:
                validated = validator(value)
                if validated != True:
                    errors.append(f"{validated}")

        validated_data[key] = value

        if isinstance(value, dict) and 'type' in rules and isinstance(rules['type'], dict):
            # Recursively validate and remove unknown keys from nested dictionaries
            nested_validated_data, nested_errors = validate_data(rules['type'], value)
            if nested_validated_data:
                validated_data[key] = nested_validated_data

            if nested_errors:
                # raise ValidationException()
                errors.extend([f"'{key}.{nested_key}': {error}" for nested_key, error in nested_errors])

    return validated_data, errors


def create_or_update_project(data:dict, pk=None):
    """
        the project info
        {
            name: "",
            repo: "",
            author: "", // repo author
            datetime: "",
        }
    """

    data_structure = {
        'name': {'type': str, 'maxlength': 30, 'required': True},
        'unique_name': {'type': str, 'maxlength': 30, 'required': True},
        'version': {'type': str, 'maxlength': 10, 'required': True},
        'about': {'type': str, 'maxlength': 100, 'required': True},
        'tags': {'type': str, 'maxlength': 100, 'required': True, 'validators': [tag_validator]},
    }

    validated_data, errors = validate_data(data_structure, data)

    collection =  db_client.collection('projects')
    
    if pk:
       return collection.document(pk).update(validated_data)

    else:
        return collection.document().set(validated_data)


def create_or_update_doc(data: dict, projectid=None, pk=None):

    """
        a sub collection of project
        data structure
            {
                version: 1,
                ln: en,
                document: "the actual document",
                indexes: [],
                user: 1 // commit author
            }
    """
    project = db_client.collection("projects").document(projectid)
    collection =  project.collection('docs')

    if pk:
       collection.document(pk).update(data)

    else:
        collection.document().add(data)


def get_project(projectid):
    return db_client.collection("projects").document(projectid).get()


def unqiue_project_name_exists(project_name):
    """
        checks if the project name already exists. returns true if the name exists
    """
    return len(db_client.collection("projects").where(filter=FieldFilter("unqiue_name", "==", project_name.lower())).limit(1).get()) > 0


def create_or_update_blog(data: dict, pk=None):

    """
        data structure:
            {
                blog: "text",
                title: "",
                user: 1,
                draft: false,
                published: false
            }
    """
    