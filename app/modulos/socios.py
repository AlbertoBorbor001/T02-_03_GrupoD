from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import random
from .validaciones import validar_cedula

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("/registrar")
def registrar_socio(nombre: str, cedula: str, db: Session = Depends(get_db)):
    # 1. Validar cédula antes de guardar
    validar_cedula(cedula)
    
    nuevo_socio = models.Socio(nombre=nombre, cedula=cedula)
    db.add(nuevo_socio)
    db.commit()
    db.refresh(nuevo_socio)
    
    # Crear cuenta automática
    nueva_cuenta = models.Cuenta(
        numero_cuenta=str(random.randint(100000, 999999)),
        saldo=0.0,
        socio_id=nuevo_socio.id
    )
    db.add(nueva_cuenta)
    db.commit()
    return {"mensaje": "Socio y Cuenta creados", "socio": nuevo_socio, "cuenta": nueva_cuenta}

@router.get("/listar")
def listar_socios(db: Session = Depends(get_db)):
    return db.query(models.Socio).all()