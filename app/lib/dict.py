from app.lib.object import present


def dict_without_blanks(some_dict: dict) -> dict:
    """ Return a dict without blank values """
    return {k: _inner_clean(v) for k, v in some_dict.items() if present(v)}


def _inner_clean(obj: object) -> object:
    if isinstance(obj, dict):
        return dict_without_blanks(obj)
    elif isinstance(obj, list):
        return [_inner_clean(element) for element in obj]
    else:
        return obj
