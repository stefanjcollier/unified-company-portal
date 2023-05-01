from app.companies.mappers.base_mapper import BaseMapper
from app.companies.mappers.extract_jurisdiction import NATION_TO_CODE
from app.companies.mappers.extract_type_from_name import ExtractTypeFromName
from app.companies.mappers.none_safe_floatify import none_safe_floatify
from app.companies.mappers.tpb.helpers import map_str_date_to_date
from app.companies.models.tpb_models import TpbRelatedCompany
from app.companies.models.unified_models import UnifiedRelatedCompany


class MapTpbToUnifiedRelatedCompany(BaseMapper):
    MODEL = UnifiedRelatedCompany

    def __init__(self, company: TpbRelatedCompany):
        self.company = company

    def _map_data(self):
        return {
            "name": self.company.name,
            "date_from": map_str_date_to_date(self.company.dateFrom),
            "date_to": map_str_date_to_date(self.company.dateTo),
            "role": self.company.type,
            "ownership_percentage": none_safe_floatify(self.company.ownership),
            "country_jurisdiction_code": NATION_TO_CODE.get(self.company.country)
        }

    def _enrich_data(self, data: dict):
        data["type"] = ExtractTypeFromName.call(data['name'])
        return data
    