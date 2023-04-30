from pydantic import ValidationError

from app.companies.errors import CannotUnifyDataException
from app.companies.models.tpb_models import TpbCompany
from app.companies.models.unified_models import UnifiedCompany
from app.companies.mappers.extract_type_from_name import ExtractTypeFromName
from app.companies.mappers.extract_active import extract_active

from .helpers import map_str_date_to_date


class MapTpbToUnifiedCompany:
    def __init__(self, tpb_company: TpbCompany):
        self.company = tpb_company

    def call(self):
        data = self._map_data()
        data = self._enrich_data(data)
        return self._to_model(data)

    def _map_data(self):
        return {
            "number": self.company.companyNumber,
            "name": self.company.companyName,
            "type": None,
            "active": None,
            "jurisdiction_code": self.company.country,
            "date_established": map_str_date_to_date(self.company.dateFrom),
            "date_dissolved": map_str_date_to_date(self.company.dateTo),
            "address": self.company.address,
            "officers": None,
            "owners": None,
        }

    def _enrich_data(self, data):
        data["type"] = ExtractTypeFromName.call(self.company.companyName)
        data["active"] = extract_active(data["date_established"], data["date_dissolved"])
        return data

    @staticmethod
    def _to_model(data: dict):
        try:
            return UnifiedCompany(**data)
        except ValidationError as e:
            raise CannotUnifyDataException(data, e)
