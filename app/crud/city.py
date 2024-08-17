from geoalchemy2.functions import (
    ST_AsText,
    ST_Distance,
    ST_X,
    ST_Y,
    ST_GeogFromText
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import City


class CRUDCity(CRUDBase):

    async def get_city_by_id(self, city_id, session: AsyncSession):
        query = select(
            City.id,
            City.name,
            ST_X(ST_AsText(City.coordinates)),
            ST_Y(ST_AsText(City.coordinates))
        ).where(City.id == city_id)
        row = await session.execute(query)
        row = row.first()
        coordinates = {
            'id': row[0],
            'name': row[1],
            'longitude': str(row[2]),
            'latitude': str(row[3])
        }
        return coordinates

    async def get_city_by_name(self, city_name, session: AsyncSession):
        query = select(
            City.id,
            City.name,
            ST_X(ST_AsText(City.coordinates)),
            ST_Y(ST_AsText(City.coordinates))
        ).where(City.name.icontains(city_name))
        rows = await session.execute(query)
        rows = rows.all()
        coordinates = [{
            'id': row[0],
            'name': row[1],
            'longitude': str(row[2]),
            'latitude': str(row[3])
        } for row in rows]
        return coordinates

    async def order_by_distance(
        self,
        longitude: str,
        latitude: str,
        session: AsyncSession
    ):
        point = f'SRID=4326;POINT({longitude} {latitude})'
        query = select(
            City.id,
            City.name,
            ST_X(ST_AsText(City.coordinates)),
            ST_Y(ST_AsText(City.coordinates))
            ).order_by(ST_Distance(City.coordinates, ST_GeogFromText(point))
                       ).limit(2).offset(1)
        result = await session.execute(query)
        result = result.all()
        result = [
            {
                'id': row[0],
                'name': row[1],
                'longitude': str(row[2]),
                'latitude': str(row[3])
            } for row in result
        ]
        return result

    async def create_city(self, obj_in, session: AsyncSession):
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return {
            'id': db_obj.id,
            'name': db_obj.name
        }


crud_city = CRUDCity(City)
