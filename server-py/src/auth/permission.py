def ensure_condition(condition):
    if condition is not True:
        raise PermissionError
