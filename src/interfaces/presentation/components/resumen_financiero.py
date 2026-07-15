from src.interfaces.presentation.context import ui
from src.interfaces.presentation.components.amortizacion_table import render_amortizacion_table


def _mostrar_resumen(container, cot, tabla, titulo):
    with container:
        ui.html(
            '<div class="av-cot-card">'
            '<div class="av-cot-step-tag">Paso 4 de 4</div>'
            f'<div class="av-cot-step-title">{titulo}</div>'
            '<div class="av-resumen-grid">'
            f'<div class="av-resumen-item"><div class="av-resumen-label">Precio del vehículo</div><div class="av-resumen-val">${cot.precio_vehiculo:,.2f}</div></div>'
            f'<div class="av-resumen-item"><div class="av-resumen-label">Entrada</div><div class="av-resumen-val">${cot.entrada:,.2f}</div></div>'
            f'<div class="av-resumen-item"><div class="av-resumen-label">Monto a financiar</div><div class="av-resumen-val">${cot.monto_financiado:,.2f}</div></div>'
            f'<div class="av-resumen-item"><div class="av-resumen-label">Tasa anual</div><div class="av-resumen-val">{cot.tasa_anual}%</div></div>'
            f'<div class="av-resumen-item"><div class="av-resumen-label">Plazo</div><div class="av-resumen-val">{cot.plazo_meses} meses</div></div>'
            f'<div class="av-resumen-item"><div class="av-resumen-label">Cuota mensual</div><div class="av-resumen-val red">${cot.cuota_mensual:,.2f}</div></div>'
            '</div></div>'
        )
        render_amortizacion_table(tabla)


def _mostrar_resultado(container, cot, tabla):
    _mostrar_resumen(container, cot, tabla, "Tu cotización · " + cot.id)


def _mostrar_resultado_estimado(container, v, p, entrada, plazo):
    from src.domain.entities.cotizacion import Cotizacion
    cot = Cotizacion(
        id="COT-DEMO",
        vehiculo_id=v.id,
        plan_id=p.id,
        nombre_cliente="Cliente",
        email_cliente="cliente@email.com",
        precio_vehiculo=v.precio_base,
        entrada=entrada,
        plazo_meses=plazo,
        tasa_anual=p.tasa_anual,
    )
    _mostrar_resumen(container, cot, cot.generar_tabla_amortizacion(), "Tu cotización")

