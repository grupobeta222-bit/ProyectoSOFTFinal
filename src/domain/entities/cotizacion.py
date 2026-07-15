from datetime import datetime
from enum import Enum
from src.domain.exceptions.domain_exception import DomainException


class EstadoCotizacion(str, Enum):
    PENDIENTE = "pendiente"
    EN_REVISION = "en_revision"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    CERRADA = "cerrada"


class Cotizacion:

    TRANSICIONES = {
        EstadoCotizacion.PENDIENTE.value: {EstadoCotizacion.EN_REVISION.value},
        EstadoCotizacion.EN_REVISION.value: {
            EstadoCotizacion.APROBADA.value,
            EstadoCotizacion.RECHAZADA.value,
        },
        EstadoCotizacion.APROBADA.value: {EstadoCotizacion.CERRADA.value},
        EstadoCotizacion.RECHAZADA.value: set(),
        EstadoCotizacion.CERRADA.value: set(),
    }

    def __init__(self, id, vehiculo_id, plan_id,
                 nombre_cliente, email_cliente,
                 precio_vehiculo, entrada, plazo_meses, tasa_anual,
                 cedula_cliente="", telefono_cliente="", ciudad_cliente="",
                 asesor_id=1, estado="pendiente", fecha=None, cliente_id=None,
                 comision_apertura=0.0, fecha_cierre=None):

        self.id = id
        self.vehiculo_id = vehiculo_id
        self.plan_id = plan_id
        self.nombre_cliente = nombre_cliente
        self.email_cliente = email_cliente
        self.cedula_cliente = cedula_cliente
        self.telefono_cliente = telefono_cliente
        self.ciudad_cliente = ciudad_cliente
        self.asesor_id = asesor_id
        self.cliente_id = cliente_id
        self.precio_vehiculo = precio_vehiculo
        self.entrada = entrada
        self.plazo_meses = plazo_meses
        self.tasa_anual = tasa_anual
        self.estado = estado
        self.comision_apertura = float(comision_apertura or 0)
        self.fecha_cierre = fecha_cierre

        if fecha is None:
            self.fecha = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        else:
            self.fecha = fecha

        self._validar()

        self.monto_financiado = self.precio_vehiculo - self.entrada
        self.cuota_mensual = self._calcular_cuota()

    @property
    def costo_inicial(self):
        return round(self.entrada + self.comision_apertura, 2)

    def _validar(self):
        if not self.id or not self.id.strip():
            raise DomainException("ID de cotizacion vacio.")

        if self.precio_vehiculo <= 0:
            raise DomainException("Precio invalido.")

        if self.entrada < 0:
            raise DomainException("Entrada invalida.")

        if self.entrada >= self.precio_vehiculo:
            raise DomainException("La entrada no puede superar el precio.")

        if self.plazo_meses <= 0:
            raise DomainException("Plazo invalido.")

        if self.tasa_anual <= 0:
            raise DomainException("Tasa invalida.")

        estados = [estado.value for estado in EstadoCotizacion]
        if self.estado not in estados:
            raise DomainException("Estado invalido: " + self.estado)

        if self.comision_apertura < 0:
            raise DomainException("La comision de apertura no puede ser negativa.")

    def transicionar(self, nuevo_estado, fecha=None):
        if isinstance(nuevo_estado, EstadoCotizacion):
            nuevo_estado = nuevo_estado.value
        permitidos = self.TRANSICIONES.get(self.estado, set())
        if nuevo_estado not in permitidos:
            raise DomainException(
                "Transicion no permitida: " + self.estado + " -> " + str(nuevo_estado)
            )
        self.estado = nuevo_estado
        if nuevo_estado == EstadoCotizacion.CERRADA.value:
            self.fecha_cierre = fecha or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return self

    def _calcular_cuota(self):
        monto = self.monto_financiado
        n = self.plazo_meses
        i = self.tasa_anual / 12 / 100

        if i == 0:
            return round(monto / n, 2)

        factor = (1 + i) ** n
        cuota = (monto * i * factor) / (factor - 1)
        return round(cuota, 2)

    def generar_tabla_amortizacion(self):
        tabla = []
        i = self.tasa_anual / 12 / 100
        saldo = self.monto_financiado
        cuota = self.cuota_mensual

        for numero in range(1, self.plazo_meses + 1):
            saldo_inicial = saldo
            interes = round(saldo_inicial * i, 2)
            if numero == self.plazo_meses:
                capital = round(saldo_inicial, 2)
                cuota_total = round(capital + interes, 2)
                saldo = 0.0
            else:
                capital = round(cuota - interes, 2)
                cuota_total = round(capital + interes, 2)
                saldo = round(saldo_inicial - capital, 2)

            tabla.append({
                "cuota": numero,
                "saldo_inicial": round(saldo_inicial, 2),
                "capital": capital,
                "interes": interes,
                "cuota_total": cuota_total,
                "saldo_final": max(saldo, 0.0),
            })

        return tabla

    def calcular_totalizadores(self):
        tabla = self.generar_tabla_amortizacion()
        total_capital = sum(f["capital"] for f in tabla)
        total_interes = sum(f["interes"] for f in tabla)
        total_pagado = sum(f["cuota_total"] for f in tabla)
        return {
            "total_capital": round(total_capital, 2),
            "total_interes": round(total_interes, 2),
            "total_pagado": round(total_pagado, 2),
        }

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "vehiculo_id": self.vehiculo_id,
            "plan_id": self.plan_id,
            "precio_vehiculo": self.precio_vehiculo,
            "entrada_monto": self.entrada,
            "monto_financiado": self.monto_financiado,
            "plazo_meses": self.plazo_meses,
            "tasa_anual": self.tasa_anual,
            "cuota_mensual": self.cuota_mensual,
            "estado": self.estado,
            "asesor_id": self.asesor_id,
            "cliente_id": self.cliente_id,
            "comision_apertura": self.comision_apertura,
            "costo_inicial": self.costo_inicial,
            "fecha_cierre": self.fecha_cierre,
            "cliente": {
                "nombre": self.nombre_cliente,
                "email": self.email_cliente,
                "cedula": self.cedula_cliente,
                "telefono": self.telefono_cliente,
                "ciudad": self.ciudad_cliente,
            },
        }

    def __str__(self):
        return self.id + " - " + self.nombre_cliente + " - cuota $" + str(self.cuota_mensual)
