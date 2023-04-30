from app.companies.mappers.base_mapper import BaseMapper
from app.companies.models.tpa_models import TpaNamedEntity, TpaShareholder, TpaOfficer
from app.companies.models.unified_models import UnifiedNameEntity

from .helpers import map_Date_to_date

def extract_name(entity: TpaNamedEntity):
    if entity.name:
        return entity.name

    name_parts = [entity.first_name, entity.middlenames, entity.last_name]
    present_name_parts = [part for part in name_parts if part]
    return ' '.join(present_name_parts)


class MapTpaNamedEntityToPerson(BaseMapper):

    MODEL = UnifiedNameEntity

    def __init__(self, entity: TpaNamedEntity):
        self.entity = entity

    def _map_data(self):
        return {
            "name": extract_name(self.entity),
            "date_from": None,
            "date_to": None,
            "role": None,
            "ownership_percentage": None
        }
