import pymysql
pymysql.install_as_MySQLdb()
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, SessionLocal, Base, get_db
import models
from modulos import socios, transacciones, prestamos
import logging

# Configuración de Auditoría (Logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema Caja de Ahorros - Grupo D (Versión Robusta)")

# Crea las tablas automáticamente
models.Base.metadata.create_all(bind=engine)

# Rutas de los módulos
app.include_router(socios.router)
app.include_router(transacciones.router)
app.include_router(prestamos.router)

@app.on_event("startup")
async def startup_event():
    logger.info(">>> SISTEMA INICIADO: Conexión con Aiven verificada.")

@app.get("/")
def inicio():
    return {"mensaje": "API Grupo D Online y Operativa"}

@app.get("/salud", tags=["Mantenimiento"])
def verificar_salud(db: Session = Depends(get_db)):
    """Ruta para verificar que la base de datos en la nube está activa."""
    try:
        db.execute(text("SELECT 1")) 
        return {"status": "online", "database": "Conectado a Aiven MySQL"}
    except Exception as e:
        print(f"Error de conexión: {e}") 
        return {"status": "error", "detalle": str(e)}