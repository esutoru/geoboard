from pydantic import BaseModel, Field

from backend.src.dashboard.types import WidgetTypes


class ExternalServiceNotAvailable(BaseModel):
    detail: str


class SearchLocationIn(BaseModel):
    query: str = Field(min_length=3, max_length=30)

    class Config:
        orm_mode = True


class WidgetIn(BaseModel):
    widget_type: WidgetTypes

    x: int
    y: int

    width: int
    height: int

    class Config:
        orm_mode = True


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


class DashboardSchema(BaseModel):
    temperature_scale: str
    location: DashboardLocationSchema
    temperature: DashboardTemperatureSchema
    condition: DashboardConditionSchema
    forecast: list[DashboardDayForecastSchema]
