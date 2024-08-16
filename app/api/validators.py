from fastapi import status
from fastapi.exceptions import HTTPException
from geoalchemy2.functions import ST_GeogFromText
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import City


async def validate_city_already_exists(WKT_coords, session: AsyncSession):
    query = select(City.id).where(
        City.coordinates == ST_GeogFromText(WKT_coords))
    do = await session.execute(query)
    do = do.scalars().first()
    if do:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Этот город уже есть в базе'
        )
