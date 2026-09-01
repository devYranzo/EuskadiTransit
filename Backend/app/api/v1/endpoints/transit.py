from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.gtfs_parser import load_gtfs_feed

router = APIRouter(prefix="/transit", tags=["Transit Data"])

@router.post("/load-gtfs/{filename}")
def trigger_gtfs_load(filename: str, db: Session = Depends(get_db)):
    try:
        result = load_gtfs_feed(filename, db)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
