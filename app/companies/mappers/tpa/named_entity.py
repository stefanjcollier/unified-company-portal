from app.companies.mappers.base_mapper import BaseMapper
from app.companies.models.tpa_models import TpaNamedEntity, TpaShareholder, TpaOfficer
from app.companies.models.unified_models import UnifiedRelatedPerson, UnifiedRelatedCompany
from app.companies.mappers.none_safe_floatify import none_safe_floatify

from .helpers import map_Date_to_date, extract_name
from ..extract_type_from_name import ExtractTypeFromName


def extra_data(entity: TpaNamedEntity):
    if isinstance(entity, TpaOfficer):
        return officer_data(entity)
    elif isinstance(entity, TpaShareholder):
        return shareholder_data(entity)
    else:
        raise NotImplementedError()


def officer_data(entity: TpaOfficer):
    return {
        "role": entity.role,
        "ownership_percentage": None
    }


def shareholder_data(entity: TpaShareholder):
    return {
        "role": "Owner",
        "ownership_percentage": none_safe_floatify(entity.shares_held)
    }


class BaseTpaNamedEntityMapper(BaseMapper):
    def __init__(self, entity: TpaNamedEntity):
        self.entity = entity

    def _map_data(self):
        data = {
            "name": extract_name(self.entity),
            "date_from": map_Date_to_date(self.entity.date_from),
            "date_to": map_Date_to_date(self.entity.date_to)
        }
        data |= extra_data(self.entity)
        return data


class MapTpaNamedEntityToPerson(BaseTpaNamedEntityMapper):
    MODEL = UnifiedRelatedPerson

    def _map_data(self):
        data = super()._map_data()
        data['dob'] = self.entity.date_of_birth
        return data


class MapTpaNamedEntityToCompany(BaseTpaNamedEntityMapper):
    MODEL = UnifiedRelatedCompany

    def _enrich_data(self, data: dict):
        data["type"] = ExtractTypeFromName.call(data['name'])
        return data