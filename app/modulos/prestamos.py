from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from .validaciones import validar_monto_positivo

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.post("/solicitar")
def solicitar_prestamo(socio_id: int, monto: float, meses: int, db: Session = Depends(get_db)):
    # 1. Validar que el préstamo no sea de $0 o negativo
    validar_monto_positivo(monto)
    
    nuevo_prestamo = models.Prestamo(monto_aprobado=monto, cuotas=meses, socio_id=socio_id)
    db.add(nuevo_prestamo)
    db.commit()
    
    valor_cuota = monto / meses
    tabla = [{"mes": i+1, "cuota": valor_cuota} for i in range(meses)]
    
    return {"mensaje": "Préstamo aprobado", "tabla_amortizacion": tabla}