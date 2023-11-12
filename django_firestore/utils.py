from typing import List, Dict, Union, Callable
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




def clean_data(data_structure, data, update=False):

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
        
        if (update and rules.get('oneoff') and key in data): # if the data is oneoff only add the value once
            addError(f"'{key}' cannot be updated", key)

        if rules.get('readonly', False) == True:
            # if the readonly is true then the user value must be discarded and default value must be used
            if check_type(rules.get('default'), Callable):
                
                if (not update or not rules.get('oneoff')): # if the data is oneoff only add the value once
                    data[key] = rules.get('default')() # continue with the validation

            else:
                raise TypeError("Invalid default value, must be a callable function")

        if key not in data and rules.get('required', False) == True and rules.get('readonly', False) == False:
            # if required is true and the key doesn't exist then raise error
            addError(f"'{key}' is required but not provided.", key)
            continue
        
        
        if (rules.get('required') == False or update) and key not in data:
            continue # don't continue with the validation if the key doesn't exist, and required is False
        
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


def convert_data_to_structure(data_structure, data: Dict[str, List[Union[str, Dict[str, str]]]]):
    """
        Given a POST request data, it will convert to a proper data format required
    """
    converted_data = {}

    for key, rules in data_structure.items():
        values = data.get(key, [])
        if 'inner' in rules:

            if isinstance(rules['inner'], dict):
                inner_data = convert_data_to_structure(rules['inner'], data)
                converted_data[key] = inner_data

            elif check_type(rules['inner'], List[Dict]):
                inner_data = []
                for x in rules['inner']:
                    inner_data.append(convert_data_to_structure(x, data))
                
                converted_data[key] = inner_data

        else:
            if values and values[0] != '':
                converted_data[key] = values[0]
                # converted_data[key] = values[0]

    return converted_data