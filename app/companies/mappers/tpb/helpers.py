from datetime import datetime

from app.companies.models.dates import PartialDate


def map_str_date_to_date(str_date: str):
    if str_date is None:
        return None

    return datetime.strptime(str_date, '%d/%m/%Y').date()


def map_str_date_to_partial_date(str_date: str):
    date = map_str_date_to_date(str_date)

    return PartialDate(year=date.year, month=date.month)
