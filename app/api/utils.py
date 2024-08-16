import requests
from fastapi import status
from fastapi.exceptions import HTTPException

from app.core.config import settings
from app.schemas.city import CityCreate


def get_city_coordinates(city_in: CityCreate):
    try:
        city_data_response = requests.get(
            settings.geo_api_url.format(
                city=city_in.name, token=settings.geo_api_token
            )
        )
    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Что-то пошло не так'
        )
    city_data = city_data_response.json()
    latitude = str(city_data[0]['lat'])
    longitude = str(city_data[0]['lon'])
    return (f'SRID=4326;POINT({longitude} {latitude})', longitude, latitude)
