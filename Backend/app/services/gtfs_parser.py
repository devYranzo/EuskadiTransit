import os
import partridge as pt
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from app.models.transit import Stop, Route, Shape

def load_gtfs_feed(feed_filename: str, db: Session):
    feed_path = os.path.join("/app", "data", "raw_gtfs", feed_filename)

    if not os.path.exists(feed_path):
        raise FileNotFoundError(f"No se encuentra el archivo GTFS: {feed_path}")

    feed = pt.load_feed(feed_path)

    # 1. Procesar Paradas
    stops_count = 0
    for _, row in feed.stops.iterrows():
        stop_id = str(row["stop_id"])
        stop_name = str(row["stop_name"])
        lat = float(row["stop_lat"])
        lon = float(row["stop_lon"])

        point_wkt = WKTElement(f'POINT({lon} {lat})', srid=4326)

        existing_stop = db.query(Stop).filter(Stop.stop_id == stop_id).first()
        if not existing_stop:
            db.add(Stop(stop_id=stop_id, stop_name=stop_name, geom=point_wkt))
            stops_count += 1

    # 2. Procesar Rutas
    routes_count = 0
    for _, row in feed.routes.iterrows():
        route_id = str(row["route_id"])
        route_short_name = str(row.get("route_short_name", ""))
        route_long_name = str(row.get("route_long_name", ""))
        route_color = str(row.get("route_color", "FFFFFF"))

        existing_route = db.query(Route).filter(Route.route_id == route_id).first()
        if not existing_route:
            db.add(Route(
                route_id=route_id,
                route_short_name=route_short_name,
                route_long_name=route_long_name,
                route_color=f"#{route_color}" if not route_color.startswith("#") else route_color
            ))
            routes_count += 1

    # 3. Procesar Trazados (Shapes) si el feed los incluye
    shapes_count = 0
    if hasattr(feed, "shapes") and feed.shapes is not None and not feed.shapes.empty:
        # Agrupar puntos por shape_id ordenados por secuencia
        grouped_shapes = feed.shapes.sort_values(["shape_id", "shape_pt_sequence"]).groupby("shape_id")

        for shape_id, group in grouped_shapes:
            coords = []
            for _, row in group.iterrows():
                coords.append(f"{float(row['shape_pt_lon'])} {float(row['shape_pt_lat'])}")

            if len(coords) >= 2:
                linestring_wkt = WKTElement(f"LINESTRING({','.join(coords)})", srid=4326)
                db.add(Shape(shape_id=str(shape_id), geom=linestring_wkt))
                shapes_count += 1

    db.commit()
    return {
        "status": "success",
        "file": feed_filename,
        "stops_imported": stops_count,
        "routes_imported": routes_count,
        "shapes_imported": shapes_count
    }
