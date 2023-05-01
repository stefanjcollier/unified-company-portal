from app.companies.mappers.base_mapper import BaseMapper
from app.companies.mappers.tpa.helpers import map_Date_to_date, map_TpaAddress_to_str
from app.companies.mappers.tpa.named_entity import MapTpaNamedEntityToPerson, MapTpaNamedEntityToCompany
from app.companies.models.tpa_models import TpaCompany, TpaNamedEntity
from app.companies.models.unified_models import UnifiedCompany



def _partition_people_and_companies(company):
    named_entities = (company.officers or []) + (company.owners or [])
    people = []
    companies = []
    for entity in named_entities:
        if entity.date_of_birth is not None:
            people.append(entity)
        else:
            companies.append(entity)
    return people, companies


def _map_status_to_active(status: str):
    return status.lower() == 'active'


def _map_people(entities: list[TpaNamedEntity]):
    return [MapTpaNamedEntityToPerson(entity).call() for entity in entities]


def _map_companies(entities: list[TpaNamedEntity]):
    return [MapTpaNamedEntityToCompany(entity).call() for entity in entities]


class MapTpaToUnifiedCompany(BaseMapper):

    MODEL = UnifiedCompany

    def __init__(self, tpa_company: TpaCompany):
        self.company = tpa_company

    def _map_data(self):
        people, companies = _partition_people_and_companies(self.company)
        return {
            "number": self.company.company_number,
            "name": self.company.company_name,
            "type": self.company.company_type,
            "active": _map_status_to_active(self.company.status),
            "jurisdiction_code": self.company.jurisdiction_code,
            "date_established": map_Date_to_date(self.company.date_established),
            "date_dissolved": map_Date_to_date(self.company.date_dissolved),
            "address": map_TpaAddress_to_str(self.company.official_address),
            "related_people": _map_people(people),
            "related_companies": _map_companies(companies)
        }

