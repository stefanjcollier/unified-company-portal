def present(value: object) -> bool:
    """ Determine if there's a not None/empty value """
    if value == False:
        return True
    return not not value
