import uuid

from src.domain.entities.cotizacion import Cotizacion


class CotizacionFactory:
    def crear(self, vehiculo, plan, cliente, entrada, plazo_meses, asesor_id):
        return Cotizacion(
            id="COT-" + str(uuid.uuid4())[:8].upper(),
            vehiculo_id=vehiculo.id,
            plan_id=plan.id,
            nombre_cliente=cliente.nombre,
            email_cliente=cliente.email,
            cedula_cliente=cliente.cedula,
            telefono_cliente=cliente.telefono,
            ciudad_cliente=cliente.ciudad,
            cliente_id=cliente.id,
            asesor_id=asesor_id,
            precio_vehiculo=vehiculo.precio_base,
            entrada=float(entrada),
            plazo_meses=int(plazo_meses),
            tasa_anual=plan.tasa_anual,
            comision_apertura=plan.comision_apertura,
            estado="pendiente",
        )
