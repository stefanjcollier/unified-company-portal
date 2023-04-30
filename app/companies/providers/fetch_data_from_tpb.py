from pydantic import ValidationError
import requests

from app.companies.errors import NotFoundException, InvalidProviderDataException
from app.companies.models.tpb_models import TpbCompany
from app.companies.mappers.tpb.company import MapTpbToUnifiedCompany


class FetchDataFromTpb:
    """
    Fetch company data from 'Third Party B'
    """
    def __init__(self, jurisdiction_code: str, company_number: str):
        self.jurisdiction_code = jurisdiction_code
        self.company_number = company_number

    def call(self):
        data = self._fetch_data()
        local_model = self._to_model(data)
        return MapTpbToUnifiedCompany(local_model).call()

    def _fetch_data(self):
        url = f"https://interview-df854r23.sikoia.com/v1/company-data?jurisdictionCode={self.jurisdiction_code}&companyNumber={self.company_number}"
        print(url)
        response = requests.get(url, headers={'Accept': 'application/json'})
        if response.status_code != 200:
            raise NotFoundException()
        return response.json()

    @staticmethod
    def _to_model(data: dict):
        try:
            return TpbCompany(**data)
        except ValidationError as e:
            raise InvalidProviderDataException(data, e)











