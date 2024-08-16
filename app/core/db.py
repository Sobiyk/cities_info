from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    declared_attr,
    DeclarativeBase,
    sessionmaker
)

from app.core.config import settings


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=True,
    class_=AsyncSession,
    autoflush=False
)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
