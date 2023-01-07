from pydantic import BaseModel, Field
from pydantic.schema import UUID

from backend.common.schema.partial import convert_to_optional
from backend.src.dashboard.types import TemperatureScales, WidgetTypes


class ExternalServiceNotAvailable(BaseModel):
    detail: str


class WidgetDoesNotFound(BaseModel):
    detail: str


class SearchLocationIn(BaseModel):
    query: str = Field(min_length=3, max_length=30)

    class Config:
        orm_mode = True


class WidgetCreateSchema(BaseModel):
    widget_type: WidgetTypes

    x: int
    y: int

    width: int
    height: int

    class Config:
        orm_mode = True


class WidgetUpdateSchema(BaseModel):
    x: int
    y: int

    width: int
    height: int

    class Config:
        orm_mode = True


class WidgetPartialUpdateSchema(WidgetUpdateSchema):
    __annotations__ = convert_to_optional(WidgetUpdateSchema)


class WidgetsBulkUpdateItemSchema(WidgetUpdateSchema):
    updated_uuid: UUID = Field(..., alias="uuid")


class WidgetsBulkUpdateSchema(BaseModel):
    widgets: list[WidgetsBulkUpdateItemSchema]


class LocationSchema(BaseModel):
    name: str
    region: str
    country: str
    code: str


class DashboardLocationSchema(BaseModel):
    name: str
    region: str
    country: str
    date: str
    time: str
    day_of_week: str


class DashboardTemperatureSchema(BaseModel):
    celsius: float
    fahrenheit: float


class DashboardConditionSchema(BaseModel):
    status: str
    icon: str


class DashboardDayForecastTemperatureSchema(BaseModel):
    max: DashboardTemperatureSchema
    min: DashboardTemperatureSchema


class DashboardDayForecastSchema(BaseModel):
    date: str
    day_of_week: str
    temperature: DashboardDayForecastTemperatureSchema
    condition: DashboardConditionSchema


class WidgetSchema(BaseModel):
    uuid: UUID
    widget_type: str

    x: int
    y: int

    width: int
    height: int

    data: dict


class DashboardSchema(BaseModel):
    temperature_scale: str
    location: DashboardLocationSchema
    temperature: DashboardTemperatureSchema
    condition: DashboardConditionSchema
    forecast: list[DashboardDayForecastSchema]
    widgets: list[WidgetSchema]


class DashboardUpdateSchema(BaseModel):
    temperature_scale: TemperatureScales
    location: str


class DashboardPartialUpdateSchema(DashboardUpdateSchema):
    __annotations__ = convert_to_optional(DashboardUpdateSchema)
