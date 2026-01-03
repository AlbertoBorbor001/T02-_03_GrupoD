from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Socio(Base):
    __tablename__ = "socios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    cedula = Column(String(10), unique=True)
    
    # NUEVO: Relación para ver sus cuentas y préstamos fácilmente
    cuentas = relationship("Cuenta", back_populates="titular")
    prestamos = relationship("Prestamo", back_populates="socio")

class Cuenta(Base):
    __tablename__ = "cuentas"
    id = Column(Integer, primary_key=True, index=True)
    numero_cuenta = Column(String(20), unique=True)
    saldo = Column(Float, default=0.0)
    socio_id = Column(Integer, ForeignKey("socios.id"))
    
    # NUEVO: Relaciones
    titular = relationship("Socio", back_populates="cuentas")
    transacciones = relationship("Transaccion", back_populates="cuenta")

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20)) # DEPOSITO o RETIRO
    monto = Column(Float)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"))
    
    # NUEVO: Relación con la cuenta
    cuenta = relationship("Cuenta", back_populates="transacciones")

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True)
    monto_aprobado = Column(Float)
    cuotas = Column(Integer)
    socio_id = Column(Integer, ForeignKey("socios.id"))
    
    # NUEVO: Relación con el socio
    socio = relationship("Socio", back_populates="prestamos")