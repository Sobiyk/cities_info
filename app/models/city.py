from geoalchemy2 import Geography
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class City(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    coordinates: Mapped[Geography] = mapped_column(
        Geography(geometry_type='POINT', srid=4326)
    )
