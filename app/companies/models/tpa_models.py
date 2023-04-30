from pydantic import BaseModel
from datetime import datetime

from .dates import Date, PartialDate


class TpaAddress(BaseModel):
    street: str
    city: str | None
    country: str | None
    postcode: str


class TpaNamedEntity(BaseModel):
    first_name: str | None = None
    middlenames: str | None = None
    last_name: str | None = None
    name: str | None = None
    date_of_birth: PartialDate | None = None
    date_from: Date | None = None
    date_to: Date | None = None


class TpaOfficer(TpaNamedEntity):
    role: str | None


class TpaShareholder(TpaNamedEntity):
    ownership_type: str | None = None
    shares_held: float | None = None


class TpaCompany(BaseModel):
    company_number: int
    company_name: str
    company_type: str
    jurisdiction_code: str
    company_type: str
    status: str
    date_established: Date | None = None
    date_dissolved: Date | None = None
    official_address: TpaAddress | None = None
    officers: list[TpaOfficer] | None = None
    owners: list[TpaShareholder] | None = None
