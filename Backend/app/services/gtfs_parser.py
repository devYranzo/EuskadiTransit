# backend/app/services/gtfs_parser.py
import os
import partridge as pt
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from app.models.transit import Stop, Route

def load_gtfs_feed(feed_filename: str, db: Session):
    """
    Procesa un archivo ZIP GTFS ubicado en data/raw_gtfs/
    y persiste las paradas y rutas en la base de datos PostGIS.
    """
    feed_path = os.path.join("/app", "data", "raw_gtfs", feed_filename)

    if not os.path.exists(feed_path):
        raise FileNotFoundError(f"No se encuentra el archivo GTFS: {feed_path}")

    # Cargar el feed filtrando fechas con partridge
    feed = pt.load_feed(feed_path)

    # 1. Procesar Paradas (stops.txt)
    stops_count = 0
    for _, row in feed.stops.iterrows():
        stop_id = str(row["stop_id"])
        stop_name = str(row["stop_name"])
        lat = float(row["stop_lat"])
        lon = float(row["stop_lon"])

        # Crear elemento geométrico espacial POINT con SRID 4326 (WGS 84)
        point_wkt = WKTElement(f'POINT({lon} {lat})', srid=4326)

        existing_stop = db.query(Stop).filter(Stop.stop_id == stop_id).first()
        if not existing_stop:
            new_stop = Stop(
                stop_id=stop_id,
                stop_name=stop_name,
                geom=point_wkt
            )
            db.add(new_stop)
            stops_count += 1

    # 2. Procesar Rutas (routes.txt)
    routes_count = 0
    for _, row in feed.routes.iterrows():
        route_id = str(row["route_id"])
        route_short_name = str(row.get("route_short_name", ""))
        route_long_name = str(row.get("route_long_name", ""))
        route_color = str(row.get("route_color", "FFFFFF"))

        existing_route = db.query(Route).filter(Route.route_id == route_id).first()
        if not existing_route:
            new_route = Route(
                route_id=route_id,
                route_short_name=route_short_name,
                route_long_name=route_long_name,
                route_color=f"#{route_color}" if not route_color.startswith("#") else route_color
            )
            db.add(new_route)
            routes_count += 1

    db.commit()
    return {
        "status": "success",
        "file": feed_filename,
        "stops_imported": stops_count,
        "routes_imported": routes_count
    }
