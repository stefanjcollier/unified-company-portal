from datetime import date
from pydantic import ValidationError

from app.companies.errors import CannotUnifyDataException
from app.companies.mappers.extract_active import extract_active
from app.companies.models.tpa_models import TpaCompany, TpaAddress
from app.companies.models.dates import Date
from app.companies.models.unified_models import UnifiedCompany


def map_Date_to_date(model: Date):
    if model is None:
        return None

    return date(model.year, model.month, model.day)


def map_TpaAddress_to_str(address: TpaAddress):
    lines = [address.street, address.city, address.country, address.postcode]
    non_empty_lines = [line for line in lines if line]
    return ', '.join(non_empty_lines)


class MapTpaToUnifiedCompany:
    def __init__(self, tpa_company: TpaCompany):
        self.company = tpa_company

    def call(self):
        data = self._map_data()
        data = self._enrich_data(data)
        return self._to_model(data)

    def _map_data(self):
        return {
            "number": self.company.company_number,
            "name": self.company.company_name,
            "type": self.company.company_type,
            "active": None,
            "jurisdiction_code": self.company.jurisdiction_code,
            "date_established": map_Date_to_date(self.company.date_established),
            "date_dissolved": map_Date_to_date(self.company.date_dissolved),
            "address": map_TpaAddress_to_str(self.company.official_address),
            "officers": None,
            "owners": None,
        }

    def _enrich_data(self, data):
        data['active'] = self.company.status == 'Active' or extract_active(data["date_established"], data["date_dissolved"])
        return data

    @staticmethod
    def _to_model(data: dict):
        try:
            return UnifiedCompany(**data)
        except ValidationError as e:
            raise CannotUnifyDataException(data, e)
