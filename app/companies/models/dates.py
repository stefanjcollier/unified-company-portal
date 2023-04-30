from pydantic import BaseModel


class PartialDate(BaseModel):
    year: int
    month: int


class Date(BaseModel):
    year: int
    month: int
    day: int

