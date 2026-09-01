from sqlalchemy import Column, String
from geoalchemy2 import Geometry
from app.core.database import Base

class Stop(Base):
    __tablename__ = "stops"

    stop_id = Column(String, primary_key=True, index=True)
    stop_name = Column(String, nullable=False)
    # Geometría espacial PostGIS para consultas por radio y proximidad
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

class Route(Base):
    __tablename__ = "routes"

    route_id = Column(String, primary_key=True, index=True)
    route_short_name = Column(String, nullable=True)
    route_long_name = Column(String, nullable=True)
    route_color = Column(String, nullable=True)
