from pydantic import ValidationError

from app.companies.errors import CannotUnifyDataException

class BaseMapper:
    MODEL = None

    def call(self):
        data = self._map_data()
        data = self._enrich_data(data)
        return self._to_model(data)

    def _map_data(self):
        raise NotImplemented

    def _enrich_data(self, data: dict):
        return data

    def _to_model(self, data: dict):
        try:
            return self.MODEL.parse_obj(data)
        except ValidationError as e:
            raise CannotUnifyDataException(data, e)

