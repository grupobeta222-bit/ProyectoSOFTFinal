from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, Numeric, String
from sqlalchemy.orm import relationship

from src.infrastructure.db_connection import Base


class VehiculoORM(Base):
    __tablename__ = "vehiculos"

    id = Column(String(20), primary_key=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)
    precio_base = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    motor = Column(String(50), nullable=True, default="N/D")
    transmision = Column(String(50), nullable=True, default="N/D")
    combustible = Column(String(30), nullable=True, default="Gasolina")
    activo = Column(Boolean, nullable=False, default=True)

    cotizaciones = relationship("CotizacionORM", back_populates="vehiculo")


class PlanFinanciamientoORM(Base):
    __tablename__ = "planes_financiamiento"

    id = Column(String(20), primary_key=True)
    nombre = Column(String(100), nullable=False)
    entrada_minima_porcentaje = Column(Numeric(5, 2), nullable=False)
    tasa_anual = Column(Numeric(5, 2), nullable=False)
    plazos_disponibles = Column(JSON, nullable=False)
    comision_apertura = Column(Numeric(10, 2), nullable=False, default=0.0)
    activo = Column(Boolean, nullable=False, default=True)

    cotizaciones = relationship("CotizacionORM", back_populates="plan")


class UsuarioORM(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password_hash = Column(String(220), nullable=False)
    rol = Column(String(20), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    especialidad = Column(String(120), nullable=True)
    rating = Column(Numeric(3, 2), nullable=False, default=0)
    foto_url = Column(String(300), nullable=True)

    cotizaciones = relationship("CotizacionORM", back_populates="asesor")


class ClienteORM(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    cedula = Column(String(20), nullable=True, unique=True)
    telefono = Column(String(20), nullable=True)
    ciudad = Column(String(60), nullable=True)
    password_hash = Column(String(220), nullable=True)
    foto_url = Column(String(300), nullable=True)
    creado_en = Column(DateTime, nullable=False, default=datetime.now)
    actualizado_en = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    cotizaciones = relationship("CotizacionORM", back_populates="cliente")
    testimonios = relationship("TestimonioORM", back_populates="cliente")


class CotizacionORM(Base):
    __tablename__ = "cotizaciones"

    id = Column(String(30), primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    vehiculo_id = Column(String(20), ForeignKey("vehiculos.id"), nullable=False)
    plan_id = Column(String(20), ForeignKey("planes_financiamiento.id"), nullable=False)
    asesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    precio_vehiculo = Column(Numeric(10, 2), nullable=False)
    entrada = Column(Numeric(10, 2), nullable=False)
    plazo_meses = Column(Integer, nullable=False)
    tasa_anual = Column(Numeric(5, 2), nullable=False)
    comision_apertura = Column(Numeric(10, 2), nullable=False, default=0)
    cuota_mensual = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), nullable=False, default="pendiente")
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    fecha_cierre = Column(DateTime, nullable=True)

    cliente = relationship("ClienteORM", back_populates="cotizaciones")
    vehiculo = relationship("VehiculoORM", back_populates="cotizaciones")
    plan = relationship("PlanFinanciamientoORM", back_populates="cotizaciones")
    asesor = relationship("UsuarioORM", back_populates="cotizaciones")


class TestimonioORM(Base):
    __tablename__ = "testimonios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    texto = Column(String(500), nullable=False)
    calificacion = Column(Integer, nullable=False, default=5)
    visible = Column(Boolean, nullable=False, default=True)
    fecha = Column(DateTime, nullable=False, default=datetime.now)

    cliente = relationship("ClienteORM", back_populates="testimonios")
