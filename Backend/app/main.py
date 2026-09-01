from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Euskadi Transit API",
    version="1.0.0",
    docs_url="/docs"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "online", "project": "Euskadi Transit Backend"}
