from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_city_coordinates
from app.api.validators import validate_city_already_exists
from app.core.db import get_async_session
from app.crud.city import crud_city
from app.schemas.city import CityCreate, CityDB

router = APIRouter()


@router.get(
    '/nearest',
    response_model=list[CityDB],
    status_code=status.HTTP_200_OK
)
async def get_two_closest_cities(
    longitude: str,
    latitude: str,
    session: AsyncSession = Depends(get_async_session)
):
    nearest_cities = await crud_city.order_by_distance(
        longitude,
        latitude,
        session
    )
    return nearest_cities


@router.get(
    '/search',
    response_model=list[CityDB],
    status_code=status.HTTP_200_OK
)
async def get_city(
    city_name: str,
    session: AsyncSession = Depends(get_async_session)
):
    city = await crud_city.get_city_by_name(city_name, session)
    return city


@router.get(
    '/{city_id}',
    response_model=CityDB,
    status_code=status.HTTP_200_OK
)
async def get_city_by_id(
    city_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    city = await crud_city.get_city_by_id(city_id, session)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Город с таким именем отсутствует в базе данных'
        )
    return city


@router.post(
    '/',
    response_model=CityDB,
    status_code=status.HTTP_201_CREATED
)
async def add_city(
    city_in: CityCreate,
    session: AsyncSession = Depends(get_async_session)
):
    WKT_coords, longitude, latitude = get_city_coordinates(city_in)
    city_in.coordinates = WKT_coords
    await validate_city_already_exists(WKT_coords, session)

    city = await crud_city.create_city(city_in, session)
    city['longitude'] = longitude
    city['latitude'] = latitude
    return city


@router.delete(
    '/{city_id}',
    status_code=status.HTTP_200_OK
)
async def remove_city(
    city_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    db_obj = await crud_city.get(city_id, session)
    if db_obj is None:
        return None
    await crud_city.remove(db_obj, session)
    return
