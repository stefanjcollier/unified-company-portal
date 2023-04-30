from pydantic import ValidationError
import requests

from app.companies.errors import NotFoundException, InvalidProviderDataException
from app.companies.models.tpa_models import TpaCompany
from app.companies.mappers.tpa.company import MapTpaToUnifiedCompany


class FetchDataFromTpa:
    """
    Fetch company data from 'Third Party A'
    """
    def __init__(self, jurisdiction_code: str, company_number: str):
        self.jurisdiction_code = jurisdiction_code
        self.company_number = company_number

    def call(self):
        data = self._fetch_data()
        local_model = self._to_model(data)
        return MapTpaToUnifiedCompany(local_model).call()

    def _fetch_data(self):
        url = f"https://interview-df854r23.sikoia.com/v1/company/{self.jurisdiction_code}/{self.company_number}"
        response = requests.get(url, headers={'Accept': 'application/json'})
        if response.status_code != 200:
            raise NotFoundException()
        return response.json()

    @staticmethod
    def _to_model(data: dict):
        try:
            return TpaCompany(**data)
        except ValidationError as e:
            raise InvalidProviderDataException(data, e)











