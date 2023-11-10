from django.db.models import QuerySet


def delete_collection(coll_ref, batch_size):

    """
        To delete an entire collection or subcollection in Cloud Firestore
    """

    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        # print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)
    

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


def clean_data(data_structure, actual_data):

    errors = []
    validated_data = {}

    for key, rules in data_structure.items():
        if key not in actual_data and rules.get('required', False):
            errors.append(f"'{key}' is required but not provided.")
            continue

        value = actual_data[key]

        if 'type' in rules and not isinstance(value, rules['type']):
            errors.append(f"'{key}' should be of type {rules['type']}.")

        if 'minlength' in rules and len(value) < rules['minlength']:
            errors.append(f"'{key}' is the below the minimum length of {rules['minlength']}.")


        if 'maxlength' in rules and len(value) > rules['maxlength']:
            errors.append(f"'{key}' exceeds the maximum length of {rules['maxlength']}.")

        if 'validators' in rules:
            for validator in rules['validators']:
                validated = validator(value)
                if validated != True:
                    errors.append(f"{validated}")

        # if isinstance(value, dict) and : 


def convert_queryset_to_datastructure(data_structure: dict, data: QuerySet):
    result = []
    
    for item in data:
        converted_item = {}
        
        for key in data_structure:
            # Assume key is the field name
            field_value = getattr(item, key, None)
            converted_item[key] = field_value
        
        result.append(converted_item)
    
    return result