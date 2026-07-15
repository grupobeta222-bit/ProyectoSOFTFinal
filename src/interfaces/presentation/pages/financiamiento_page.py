from src.interfaces.presentation.context import get_planes, ui
from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav


def ir_cotizar():
    ui.navigate.to("/cotizar")


def texto_plazos(plazos):
    texto = ""
    for plazo in plazos:
        if texto:
            texto = texto + ", "
        texto = texto + str(plazo)
    return texto


def mostrar_plan(plan):
    ui.html(f'''
    <div class="av-finance-card">
      <h3>{plan.nombre}</h3>
      <p>Plan disponible para clientes que desean financiar su vehículo con pagos mensuales.</p>
      <div class="av-finance-list">
        • Entrada mínima: <strong style="color:#fff;">{plan.entrada_minima_porcentaje}%</strong><br>
        • Tasa anual: <strong style="color:#e63946;">{plan.tasa_anual}%</strong><br>
        • Plazos: <strong style="color:#fff;">{texto_plazos(plan.plazos_disponibles)} meses</strong><br>
        • Comisión apertura: <strong style="color:#fff;">${plan.comision_apertura:,.0f}</strong>
      </div>
    </div>
    ''')


def financiamiento():
    nav("financiamiento")
    planes = get_planes()

    with ui.element("div").style("padding-top:110px;"):
        with ui.element("div").classes("av-section"):
            ui.html('<div class="av-tag">Opciones de pago</div>')
            ui.html('<h2 class="av-h2">Planes de financiamiento</h2>')
            ui.html('''
            <p style="font-size:15px;color:#777;line-height:1.7;margin-top:-24px;
                      margin-bottom:32px;max-width:680px;">
              Compara los planes disponibles y elige el que mejor se ajuste a tu
              presupuesto. Luego puedes usar el cotizador para calcular tu cuota mensual.
            </p>
            ''')

            with ui.element("div").classes("av-finance-grid"):
                for plan in planes:
                    mostrar_plan(plan)

            ui.button("Calcular una cotización", on_click=ir_cotizar).classes(
                "av-btn-p"
            ).style("margin-top:32px;")

    footer()
