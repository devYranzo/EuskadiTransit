from fastapi import APIRouter
from app.api.v1.endpoints import transit

api_router = APIRouter()
api_router.include_router(transit.router)
