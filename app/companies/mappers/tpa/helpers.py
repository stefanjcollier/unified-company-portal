from datetime import date

from app.companies.models.dates import Date
from app.companies.models.tpa_models import TpaAddress


def map_Date_to_date(model: Date):
    if model is None:
        return None

    return date(model.year, model.month, model.day)


def map_TpaAddress_to_str(address: TpaAddress):
    lines = [address.street, address.city, address.country, address.postcode]
    non_empty_lines = [line for line in lines if line]
    return ', '.join(non_empty_lines)


