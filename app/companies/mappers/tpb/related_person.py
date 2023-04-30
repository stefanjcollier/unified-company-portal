from app.companies.mappers.base_mapper import BaseMapper
from app.companies.mappers.extract_jurisdiction import NATION_TO_CODE
from app.companies.mappers.none_safe_floatify import none_safe_floatify
from app.companies.mappers.tpb.helpers import map_str_date_to_date, map_str_date_to_partial_date
from app.companies.models.tpb_models import TpbRelatedPerson
from app.companies.models.unified_models import UnifiedRelatedPerson


class MapTpbToUnifiedPerson(BaseMapper):
    MODEL = UnifiedRelatedPerson

    def __init__(self, person: TpbRelatedPerson):
        self.person = person

    def _map_data(self):
        return {
            "name": self.person.name,
            "date_from": map_str_date_to_date(self.person.dateFrom),
            "date_to": map_str_date_to_date(self.person.dateTo),
            "role": self.person.type,
            "ownership_percentage": none_safe_floatify(self.person.ownership),
            "dob": map_str_date_to_partial_date(self.person.birthDate),
            "nationality_jurisdiction_code": NATION_TO_CODE.get(self.person.nationality)
        }
