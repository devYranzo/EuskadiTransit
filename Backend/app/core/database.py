import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://euskadi_user:euskadi_password@db:5432/euskadi_transit")

# Bucle de reintentos para esperar a que PostGIS esté listo
engine = None
while engine is None:
    try:
        temp_engine = create_engine(DATABASE_URL)
        with temp_engine.connect() as conn:
            print("¡Conexión exitosa con la base de datos PostGIS!")
        engine = temp_engine
    except OperationalError:
        print("La base de datos se está iniciando, esperando 2 segundos...")
        time.sleep(2)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
