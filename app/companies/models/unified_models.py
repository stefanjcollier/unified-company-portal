from pydantic import BaseModel
from datetime import date

from app.companies.models.dates import PartialDate


class UnifiedNameEntity(BaseModel):
    name: str
    date_from: date | None = None
    date_to: date | None = None
    role: str | None = None
    ownership_percentage: float | None = None


class UnifiedRelatedPerson(UnifiedNameEntity):
    dob: PartialDate | None = None
    nationality_jurisdiction_code: str | None = None


class UnifiedRelatedCompany(UnifiedNameEntity):
    country_jurisdiction_code: str | None = None


class UnifiedCompany(BaseModel):
    number: str
    name: str
    type: str | None
    active: bool | None = None
    jurisdiction_code: str
    date_established: date | None = None
    date_dissolved: date | None = None
    address: str
    related_people: list[UnifiedRelatedPerson] = []
    related_companies: list[UnifiedRelatedCompany] = []
