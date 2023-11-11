from typing import List, Dict
from typeguard import check_type as _check_type, TypeCheckError


class ErrorDict:

    def __init__(self, error: dict) -> None:
        self.error = error

    def __iter__(self):
        return self.error
    
    def as_dict(self):
        return self.error


def check_type(data, data_type):

    try:
        _check_type(data, data_type)
        return True
    
    except TypeCheckError:
        return False


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
    

# def validate_data(data_structure, actual_data):
#     errors = []
#     validated_data = {}

#     for key, rules in data_structure.items():
#         if key not in actual_data:
#             if rules.get('required', False):
#                 errors.append(f"'{key}' is required but not provided.")
#             continue

#         value = actual_data[key]

#         if 'type' in rules:
            
#             try:
#                 check_type(value, rules['type'])
#             except TypeCheckError as e:
#                 errors.append(f"'{key}' should be of type {rules['type']}.")

#         if 'maxlength' in rules and len(value) > rules['maxlength']:
#             errors.append(f"'{key}' exceeds the maximum length of {rules['maxlength']} characters.")

#         if 'validators' in rules:
#             for validator in rules['validators']:
#                 validated = validator(value)
#                 if validated != True:
#                     errors.append(f"{validated}")

#         validated_data[key] = value

#         if isinstance(value, dict) and 'type' in rules and isinstance(rules['type'], dict):
#             # Recursively validate and remove unknown keys from nested dictionaries
#             nested_validated_data, nested_errors = validate_data(rules['type'], value)
#             if nested_validated_data:
#                 validated_data[key] = nested_validated_data

#             if nested_errors:
#                 # raise ValidationException()
#                 errors.extend([f"'{key}.{nested_key}': {error}" for nested_key, error in nested_errors])

#     return validated_data, errors




def clean_data(data_structure, data):

    errors = {}
    validated_data = {}

    def addError(error, key):
        if key in errors:

            if isinstance(error, list):
                errors[key].extends(error)

            else:
                errors[key].append(error)

        else:
            errors[key] = [error]

    # print("Data: ", data, type(data))

    for key, rules in data_structure.items():
        

        if key not in data and rules.get('required', False) == True:
            addError(f"'{key}' is required but not provided.", key)
            continue
        
        # print("rules: ", key, rules)
        
        if rules.get('required') == False and key not in data:
            continue # don't continue with the validation if the key doesn't exist
        
        else:
            value = data[key] # if it exists continue with the validation


        if 'type' in rules and not check_type(value, rules['type']):
            addError(f"'{key}' should be of type {rules['type']}.", key)

        if 'minlength' in rules and len(value) < rules['minlength']:
            addError(f"'{key}' is the below the minimum length of {rules['minlength']}.", key)

        if 'maxlength' in rules and len(value) > rules['maxlength']:
            addError(f"'{key}' exceeds the maximum length of {rules['maxlength']}.", key)

        if 'validators' in rules:
            for validator in rules['validators']:
                validated = validator(value)
                if validated != True:
                    addError(f"{validated}", key)

        validated_data[key] = value

        if 'inner' in rules:

            if isinstance(rules['inner'], dict):
                nested_validated_data, nested_errors = clean_data(rules['inner'], value)
    
                # print("validated: ",  nested_validated_data, nested_errors)
                if nested_validated_data:
                    validated_data[key] = nested_validated_data

                if nested_errors:
                    # raise ValidationException()
                    addError([f"'{key}' has {error}" for error in nested_errors], key)

            elif check_type(rules['inner'], List[Dict]):

                _rule = rules['inner']

                if rules['repeat'] and len(value) > 1:
                    _rule.extend(_rule*len(value))

                for idx, x in enumerate(_rule):
                    # print("validated: ", x, value, end="\n\n")
                    nested_validated_data, nested_errors = clean_data(x, value[idx])

                    if nested_validated_data:
                        validated_data[key] = nested_validated_data

                    if nested_errors:
                        # raise ValidationException()
                        addError(nested_errors, key)


    return validated_data, errors


def convert_to_datastructure(data_structure: dict, data: dict):
    result = []
    
    for item in data:
        converted_item = {}
        
        for key in data_structure:
            # Assume key is the field name
            field_value = getattr(item, key, None)
            converted_item[key] = field_value
        
        result.append(converted_item)
    
    return result