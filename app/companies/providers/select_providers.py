from types import MappingProxyType as ImmutableDict

from app.companies.errors import UnsupportedJurisdictionException
from app.companies.providers.fetch_data_from_tpa import FetchDataFromTpa
from app.companies.providers.fetch_data_from_tpb import FetchDataFromTpb


class SelectProviders(object):

    # Idea:
    JURISDICTION_TO_PROVIDERS = ImmutableDict({
        "uk": [FetchDataFromTpa],
        "de": [FetchDataFromTpa, FetchDataFromTpb],
        "nl": [FetchDataFromTpb],
    })

    @classmethod
    def call(cls, jurisdiction_code: str):
        providers = cls.JURISDICTION_TO_PROVIDERS.get(jurisdiction_code, [])
        if not providers:
            raise UnsupportedJurisdictionException()

        return providers


