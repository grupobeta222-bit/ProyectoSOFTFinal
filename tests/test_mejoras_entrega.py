from unittest.mock import Mock

import pytest

from src.application.services.contacto_service import ContactoService
from src.application.services.dashboard_service import DashboardService
from src.domain.entities.cotizacion import Cotizacion
from src.domain.exceptions.domain_exception import DomainException
from src.infrastructure.security import hash_password, verify_password


def crear_cotizacion(estado="pendiente", precio=25000, comision=200):
    return Cotizacion(
        id="COT-PRUEBA",
        vehiculo_id="VEH001",
        plan_id="PLAN001",
        nombre_cliente="Cliente Prueba",
        email_cliente="cliente@prueba.com",
        precio_vehiculo=precio,
        entrada=5000,
        plazo_meses=24,
        tasa_anual=12,
        estado=estado,
        comision_apertura=comision,
    )


def test_password_se_guarda_como_hash():
    password_hash = hash_password("Clave123")
    assert "Clave123" not in password_hash
    assert verify_password("Clave123", password_hash)
    assert not verify_password("Incorrecta", password_hash)


def test_flujo_de_estado_valido():
    cotizacion = crear_cotizacion()
    cotizacion.transicionar("en_revision")
    cotizacion.transicionar("aprobada")
    cotizacion.transicionar("cerrada")
    assert cotizacion.estado == "cerrada"
    assert cotizacion.fecha_cierre


def test_flujo_no_permite_saltar_estados():
    with pytest.raises(DomainException):
        crear_cotizacion().transicionar("cerrada")


def test_dashboard_solo_cuenta_cerradas_como_ventas():
    repo = Mock()
    usuarios = Mock()
    servicio = DashboardService(repo, usuarios)
    resumen = servicio.resumen([
        crear_cotizacion("aprobada", 25000, 200),
        crear_cotizacion("cerrada", 30000, 300),
    ])
    assert resumen["cerradas"] == 1
    assert resumen["ingresos"] == 30000
    assert resumen["comisiones"] == 300


def test_amortizacion_termina_en_cero():
    tabla = crear_cotizacion().generar_tabla_amortizacion()
    assert tabla[-1]["saldo_final"] == 0
    assert round(sum(fila["capital"] for fila in tabla), 2) == 20000


def test_contacto_usa_whatsapp_y_correo_acordados():
    servicio = ContactoService()
    assert "593986698212" in servicio.enlace_whatsapp()
    assert servicio.enlace_correo().startswith("mailto:grupobeta222@gmail.com")
