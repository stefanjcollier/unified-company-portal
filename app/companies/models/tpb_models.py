from pydantic import BaseModel


class TbpActivity(BaseModel):
    activityCode: int
    activityDescription: str


class TpbNamedEntity(BaseModel):
    name: str
    dateFrom: str | None = None
    dateTo: str | None = None
    type: str | None = None
    ownership: str | None = None
    birthDate: str | None = None


class TpbRelatedPerson(TpbNamedEntity):
    nationality: str


class TpbRelatedCompany(BaseModel):
    name: str
    dateFrom: str
    dateTo: str | None = None
    address: str | None = None
    type: str | None = None
    country: str | None = None
    ownership: str | None = None


class TpbCompany(BaseModel):
    companyNumber: int
    companyName: str
    country: str
    dateFrom: str | None = None
    dateTo: str | None = None
    address: str | None = None
    activities: list[TbpActivity] | None = []
    relatedPersons: list[TpbRelatedPerson]
    relatedCompanies: list[TpbRelatedCompany]
