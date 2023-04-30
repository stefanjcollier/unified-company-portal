from app.companies.providers.select_providers import SelectProviders


class FetchData:
    def __init__(self, jurisdiction_code: str, company_number: str):
        self.jurisdiction_code = jurisdiction_code
        self.company_number = company_number

    def call(self):
        providers = SelectProviders.call(self.jurisdiction_code)
        models = [self._fetch_data(provider) for provider in providers]
        return self._consolidate_models(models)

    def _fetch_data(self, provider):
        return provider(self.jurisdiction_code, self.company_number).call()

    @staticmethod
    def _consolidate_models(models):
        for model in models:
            if model:
                return model
