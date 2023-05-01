from app.companies.providers.select_providers import SelectProviders
from app.companies.consolidators.consolidate import consolidate_companies


class FetchData:
    def __init__(self, jurisdiction_code: str, company_number: str):
        self.jurisdiction_code = jurisdiction_code
        self.company_number = company_number

    def call(self):
        providers = SelectProviders.call(self.jurisdiction_code)
        models = [self._fetch_data(provider) for provider in providers]
        return consolidate_companies(models)

    def _fetch_data(self, provider):
        # TODO add some handling for when the company isn't in both providers
        return provider(self.jurisdiction_code, self.company_number).call()
