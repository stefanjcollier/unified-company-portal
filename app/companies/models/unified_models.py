from pydantic import BaseModel
from datetime import date

from app.companies.models.dates import PartialDate


class UnifiedCompany(BaseModel):
    number: str
    name: str
    type: str | None
    active: bool | None = None
    jurisdiction_code: str
    date_established: date | None = None
    date_dissolved: date | None = None
    address: str
    officers: list[str] | None = None
    owners: list[str] | None = None


class UnifiedNameEntity(BaseModel):
    name: str
    nationality_jurisdiction_code: str | None
    date_from: date | None = None
    date_to: date | None = None
    dob: PartialDate | None = None


class UnifiedOfficer(UnifiedNameEntity):
    role: str | None
