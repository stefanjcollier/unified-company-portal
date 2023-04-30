from datetime import datetime


def map_str_date_to_date(str_date: str):
    if str_date is None:
        return None

    return datetime.strptime(str_date, '%d/%m/%Y').date()
