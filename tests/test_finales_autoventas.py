from src.domain.entities.cliente import Cliente
from src.domain.entities.cotizacion import Cotizacion


def test_cliente_guarda_ciudad():
    cliente = Cliente(
        nombre="Juan Perez",
        email="juan@mail.com",
        cedula="0912345678",
        telefono="0991234567",
        ciudad="Guayaquil",
    )
    assert cliente.ciudad == "Guayaquil"


def test_totalizadores_amortizacion():
    cot = Cotizacion(
        id="COT-TEST",
        vehiculo_id="VEH001",
        plan_id="PLAN001",
        nombre_cliente="Juan Perez",
        email_cliente="juan@mail.com",
        precio_vehiculo=25990.0,
        entrada=6000.0,
        plazo_meses=12,
        tasa_anual=12.5,
    )
    totales = cot.calcular_totalizadores()
    assert totales["total_capital"] > 0
    assert totales["total_interes"] > 0
    assert totales["total_pagado"] > 0
