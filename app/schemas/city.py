from pydantic import BaseModel, Field


class CityCreate(BaseModel):
    name: str
    coordinates: str = Field(None)


class CityDB(BaseModel):
    id: int
    name: str
    longitude: str
    latitude: str


class Coordinates(BaseModel):
    longitude: str
    latitude: str
