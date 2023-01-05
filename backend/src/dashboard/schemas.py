from pydantic import BaseModel, Field


class ExternalServiceNotAvailable(BaseModel):
    detail: str


class SearchLocationIn(BaseModel):
    query: str = Field(min_length=3, max_length=30)

    class Config:
        orm_mode = True


class LocationSchema(BaseModel):
    name: str
    region: str
    country: str
    code: str
