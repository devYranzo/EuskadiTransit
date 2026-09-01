from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(prefix="/stops", tags=["Stops"])

@router.get("/nearby")
def get_nearby_stops(
    lat: float = Query(..., description="Latitud del usuario"),
    lon: float = Query(..., description="Longitud del usuario"),
    radius: float = Query(1000, description="Radio de búsqueda en metros"),
    db: Session = Depends(get_db)
):
    """
    Busca paradas en un radio determinado usando funciones espaciales de PostGIS.
    """
    # Consulta SQL nativa optimizada para PostGIS usando conversiones de geografía en metros
    query = text("""
        SELECT stop_id, stop_name, ST_X(geom) as lon, ST_Y(geom) as lat,
               ST_Distance(geom::geography, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography) as distance_meters
        FROM stops
        WHERE ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, :radius)
        ORDER BY distance_meters ASC
        LIMIT 20;
    """)

    result = db.execute(query, {"lon": lon, "lat": lat, "radius": radius}).fetchall()

    stops = []
    for row in result:
        stops.append({
            "stop_id": row.stop_id,
            "stop_name": row.stop_name,
            "lon": row.lon,
            "lat": row.lat,
            "distance_meters": round(row.distance_meters, 1)
        })

    return {"count": len(stops), "stops": stops}
