
# Idea: get this from a 3rd party provider or Open Source Dataset
_NATIONS = [
    ['Braavos', 'Braavosi', 'got-br'],
    ['Westeros', 'Westerosi', 'got-we'],
    ['Pentos', 'Pentoshi', 'got-pe'],
    ['United States', 'American', 'us'],
    ['Italy', 'Italian', 'it'],
    ['Canada', 'Canadian', 'ca'],
    ['Netherlands', 'Dutch', 'nl'],
    ['Germany', 'German', 'de'],
    ['Great Britain', 'British', 'gb'],
    ['Japan', 'Japanese', 'jp'],
    ['France', 'French', 'fr'],
]


def _generate_map(nations: list[list[str]]):
    map = {}
    for nation, nationality, code in nations:
        map[nation] = code
        map[nationality] = code
    return map


NATION_TO_CODE = _generate_map(_NATIONS)
