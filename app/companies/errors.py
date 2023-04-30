

class CompanyException(Exception):
    pass


class NotFoundException(CompanyException):
    pass


class InvalidProviderDataException(CompanyException):
    def __init__(self, data, errors):
        self.data = data
        self.errors = errors


class CannotUnifyDataException(CompanyException):
    def __init__(self, data, errors):
        self.data = data
        self.errors = errors


class UnsupportedJurisdictionException(CompanyException):
    pass
