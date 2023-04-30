from app.companies.mappers.base_mapper import BaseMapper
from app.companies.models.tpa_models import TpaNamedEntity, TpaShareholder, TpaOfficer
from app.companies.models.unified_models import UnifiedRelatedPerson, UnifiedRelatedCompany

from .helpers import none_safe_floatify, map_Date_to_date, extract_name


def map_common_entity_data(entity: TpaNamedEntity):
    return {
        "name": extract_name(entity),
        "date_from": map_Date_to_date(entity.date_from),
        "date_to": map_Date_to_date(entity.date_to)
    }


def extra_data(entity: TpaNamedEntity):
    if isinstance(entity, TpaOfficer):
        return officer_data(entity)
    elif isinstance(entity, TpaShareholder):
        return shareholder_data(entity)
    else:
        raise NotImplemented()


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
        data = map_common_entity_data(self.entity)
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
