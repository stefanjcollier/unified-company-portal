from app.companies.models.tpa_models import TpaNamedEntity, TpaShareholder, TpaOfficer

class MapTpaNamedEntityToPerson:
    def __init__(self, entity: TpaNamedEntity):
        self.entity = entity

    def call(self):
        data = self._map_data()