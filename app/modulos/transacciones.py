from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from .validaciones import validar_monto_positivo, validar_saldo_suficiente

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/operacion")
def realizar_transaccion(cuenta_id: int, tipo: str, monto: float, db: Session = Depends(get_db)):
    # 1. Validar monto positivo
    validar_monto_positivo(monto)
    
    cuenta = db.query(models.Cuenta).filter(models.Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    tipo_up = tipo.upper()
    if tipo_up == "RETIRO":
        # 2. Validar si hay dinero suficiente
        validar_saldo_suficiente(cuenta.saldo, monto)
        cuenta.saldo -= monto
    elif tipo_up == "DEPOSITO":
        cuenta.saldo += monto
    else:
        raise HTTPException(status_code=400, detail="Tipo de operación inválida (DEPOSITO/RETIRO)")
    
    nueva_transaccion = models.Transaccion(tipo=tipo_up, monto=monto, cuenta_id=cuenta_id)
    db.add(nueva_transaccion)
    db.commit()
    return {"mensaje": "Transacción exitosa", "nuevo_saldo": cuenta.saldo}