import json

def is_null_or_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value
    elif isinstance(value, (list, tuple, set)):
        return not value
    else:
        return False
