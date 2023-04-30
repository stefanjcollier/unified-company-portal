from pydantic import ValidationError

from app.companies.errors import CannotUnifyDataException
from app.companies.models.tpb_models import TpbCompany, TpbNamedEntity, TpbRelatedPerson
from app.companies.models.unified_models import UnifiedCompany
from app.companies.mappers.extract_type_from_name import ExtractTypeFromName
from app.companies.mappers.extract_active import extract_active

from .helpers import map_str_date_to_date
from .related_company import MapTpbToUnifiedRelatedCompany
from .related_person import MapTpbToUnifiedPerson
from ..base_mapper import BaseMapper


def _map_people(people: list[TpbRelatedPerson]):
    return [MapTpbToUnifiedPerson(person).call() for person in people]


def _map_companies(companies: list[TpbNamedEntity]):
    return [MapTpbToUnifiedRelatedCompany(company).call() for company in companies]


class MapTpbToUnifiedCompany(BaseMapper):

    MODEL = UnifiedCompany

    def __init__(self, tpb_company: TpbCompany):
        self.company = tpb_company

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
            "related_people": _map_people(self.company.relatedPersons),
            "related_companies": _map_companies(self.company.relatedCompanies),
        }

    def _enrich_data(self, data):
        data["type"] = ExtractTypeFromName.call(self.company.companyName)
        data["active"] = extract_active(data.get("date_established"), data.get("date_dissolved"))
        return data
