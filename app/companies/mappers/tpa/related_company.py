from app.companies.mappers.base_mapper import BaseMapper
from app.companies.models.tpa_models import TpaShareholder, TpaOfficer, TpaNamedEntity
from app.companies.models.unified_models import UnifiedCompany

from .helpers import map_common_entity_data, none_safe_floatify





class MapTpaNamedEntityToCompany(BaseMapper):

    MODEL = UnifiedCompany

    def __init__(self, entity: TpaNamedEntity):
        self.entity = entity

    def _map_data(self):
        data = map_common_entity_data(self.entity)

        return data

        if isinstance(self.entity, TpaOfficer):
            data += map_officer_to_company(self.entity)
        elif isinstance(self.entity, TpaShareholder):
            return _map_shareholder_to_company(self.entity)
        else:
            raise NotImplemented()
