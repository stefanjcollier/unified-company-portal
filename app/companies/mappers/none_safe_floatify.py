def none_safe_floatify(string):
    if string is None:
        return None

    return float(string)
