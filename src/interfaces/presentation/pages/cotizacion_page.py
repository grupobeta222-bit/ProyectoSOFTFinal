from html import escape

from src.interfaces.presentation.components.cliente_form import crear_campos_cliente
from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.components.resumen_financiero import _mostrar_resultado
from src.interfaces.presentation.context import (
    generar_cotizacion_segura,
    get_cliente_actual,
    get_planes,
    get_vehiculos,
    ui,
)
from src.interfaces.presentation.pdf_cotizacion import generar_pdf_cotizacion


class CotizacionPage:
    def __init__(self):
        self.vehiculos = []
        self.planes = []
        self.ultima_cotizacion = None
        self.ultima_tabla = None

    def render(self):
        nav("cotizar")
        self.vehiculos = get_vehiculos()
        self.planes = get_planes()
        vehiculo_url = self._vehiculo_en_url()
        if self._buscar(self.vehiculos, vehiculo_url) is None:
            vehiculo_url = None

        with ui.element("div").classes("wizard-wrap"):
            ui.html('<div style="font-size:32px;font-weight:800;color:#fff;letter-spacing:-1px;margin-bottom:6px;">Cotizador financiero</div>')
            ui.html('<div style="font-size:14px;color:#777;margin-bottom:32px;">Calcula la cuota y revisa la amortización antes de enviar tus datos.</div>')
            self._paso_vehiculo(vehiculo_url)
            self._paso_plan()
            self._paso_cliente()
            self.mensaje = ui.html("")
            self.resultado = ui.element("div")
            ui.button("Generar cotización", on_click=self.calcular).style(
                "width:100%;background:#e63946;color:#fff;border:none;padding:16px;"
                "font-size:16px;font-weight:800;border-radius:12px;margin:10px 0 20px;"
                "text-transform:none;box-shadow:none;"
            )
        footer()

    def _paso_vehiculo(self, vehiculo_url):
        with ui.element("div").classes("av-cot-card"):
            ui.html('<div class="av-cot-step-tag">Paso 1 de 4</div>')
            ui.html('<div class="av-cot-step-title">Selecciona el vehículo</div>')
            opciones = {
                item.id: f"{item.marca} {item.modelo} {item.anio} - ${item.precio_base:,.0f}"
                for item in self.vehiculos if item.activo
            }
            self.sel_vehiculo = ui.select(
                opciones, label="Vehículo", value=vehiculo_url
            ).props("outlined stack-label").style("width:100%;")
            self.sel_vehiculo.on("update:model-value", self._actualizar_entrada)

    def _paso_plan(self):
        with ui.element("div").classes("av-cot-card"):
            ui.html('<div class="av-cot-step-tag">Paso 2 de 4</div>')
            ui.html('<div class="av-cot-step-title">Elige el plan de financiamiento</div>')
            for plan in self.planes:
                plazos = ", ".join(str(item) for item in plan.plazos_disponibles)
                ui.html(f'''<div class="av-choice-card">
                  <div class="av-choice-title">{escape(plan.nombre)}</div>
                  <div class="av-choice-text">Entrada mínima: {plan.entrada_minima_porcentaje}% · Tasa anual: {plan.tasa_anual}%</div>
                  <div class="av-choice-text">Plazos: {plazos} meses · Comisión de apertura: ${plan.comision_apertura:,.2f}</div>
                </div>''')
            with ui.element("div").classes("av-form-space"):
                opciones = {"": "Seleccione un plan"}
                opciones.update({item.id: f"{item.nombre} - {item.tasa_anual}% anual" for item in self.planes if item.activo})
                self.sel_plan = ui.select(
                    opciones, label="Plan de financiamiento", value=""
                ).props("outlined stack-label")
                self.sel_plazo = ui.select(
                    {"": "Seleccione un plazo"}, label="Plazo", value=""
                ).props("outlined stack-label")
                self.sel_plazo.disable()
            self.resumen_plan = ui.html("")
            self.sel_plan.on("update:model-value", self._actualizar_plan)
            self.sel_plazo.on("update:model-value", self._actualizar_resumen)

    def _paso_cliente(self):
        with ui.element("div").classes("av-cot-card"):
            ui.html('<div class="av-cot-step-tag">Paso 3 de 4</div>')
            ui.html('<div class="av-cot-step-title">Entrada y datos de contacto</div>')
            with ui.element("div").classes("av-form-space"):
                self.inp_entrada = ui.number(
                    label="Monto de entrada ($)", value=None, min=0, step=500
                ).props('outlined stack-label placeholder="Ejemplo: 5000"')
            campos = crear_campos_cliente()
            self.inp_nombre, self.inp_email, self.inp_cedula, self.inp_telefono, self.inp_ciudad = campos
            cliente = get_cliente_actual()
            if cliente:
                self.inp_nombre.value = cliente.get("nombre", "")
                self.inp_email.value = cliente.get("email", "")
                self.inp_cedula.value = cliente.get("cedula", "")
                self.inp_telefono.value = cliente.get("telefono", "")

    def _actualizar_plan(self, _evento=None):
        plan = self._buscar(self.planes, self.sel_plan.value)
        if plan is None:
            self.sel_plazo.options = {"": "Seleccione un plazo"}
            self.sel_plazo.value = ""
            self.sel_plazo.disable()
        else:
            self.sel_plazo.options = {item: f"{item} meses" for item in plan.plazos_disponibles}
            self.sel_plazo.value = plan.plazos_disponibles[0]
            self.sel_plazo.enable()
        self.sel_plazo.update()
        self._actualizar_resumen()
        self._actualizar_entrada()

    def _actualizar_resumen(self, _evento=None):
        plan = self._buscar(self.planes, self.sel_plan.value)
        if plan is None:
            self.resumen_plan.set_content("")
            return
        plazo = f"{self.sel_plazo.value} meses" if self.sel_plazo.value else "Pendiente"
        self.resumen_plan.set_content(f'''<div class="av-selected-grid">
          <div class="av-selected-box">
            <div class="av-selected-label">Plan seleccionado</div>
            <div class="av-selected-value">{escape(plan.nombre)}</div>
            <div class="av-choice-text">Tasa anual: {plan.tasa_anual}%</div>
          </div>
          <div class="av-selected-box">
            <div class="av-selected-label">Plazo seleccionado</div>
            <div class="av-selected-value">{plazo}</div>
          </div>
        </div>''')

    def _actualizar_entrada(self, _evento=None):
        if not hasattr(self, "inp_entrada"):
            return
        plan = self._buscar(self.planes, self.sel_plan.value)
        vehiculo = self._buscar(self.vehiculos, self.sel_vehiculo.value)
        if plan is None or vehiculo is None:
            return
        minima = vehiculo.precio_base * plan.entrada_minima_porcentaje / 100
        self.inp_entrada.min = minima
        if self.inp_entrada.value is None or float(self.inp_entrada.value) < minima:
            self.inp_entrada.value = minima
        self.inp_entrada.props(f'outlined stack-label placeholder="Mínimo: ${minima:,.0f}"')
        self.inp_entrada.update()

    def calcular(self):
        self.mensaje.set_content("")
        self.resultado.clear()
        error = self._validar_formulario()
        if error:
            self.mensaje.set_content(f'<div class="av-alert-err">{error}</div>')
            return
        try:
            cotizacion, tabla, _guardado = generar_cotizacion_segura(
                vehiculo_id=self.sel_vehiculo.value,
                plan_id=self.sel_plan.value,
                nombre_cliente=self.inp_nombre.value,
                email_cliente=self.inp_email.value,
                cedula_cliente=self.inp_cedula.value or "",
                telefono_cliente=self.inp_telefono.value or "",
                ciudad_cliente=self.inp_ciudad.value or "",
                entrada=float(self.inp_entrada.value or 0),
                plazo_meses=int(self.sel_plazo.value),
            )
            self.ultima_cotizacion = cotizacion
            self.ultima_tabla = tabla
            _mostrar_resultado(self.resultado, cotizacion, tabla)
            with self.resultado:
                ui.button("Descargar cotización PDF", on_click=self.descargar_pdf).classes("av-btn-s").style("width:100%;margin-top:10px;")
            self.mensaje.set_content('<div class="av-alert-ok">Cotización generada y guardada. Un asesor podrá revisarla.</div>')
        except Exception as error:
            self.mensaje.set_content(f'<div class="av-alert-err">{escape(str(error))}</div>')

    def _validar_formulario(self):
        if not self.sel_vehiculo.value:
            return "Selecciona un vehículo."
        if not self.sel_plan.value:
            return "Selecciona un plan."
        if not self.sel_plazo.value:
            return "Selecciona un plazo."
        if not self.inp_nombre.value or not self.inp_email.value:
            return "Completa nombre y correo electrónico."
        return ""

    def descargar_pdf(self):
        if not self.ultima_cotizacion or not self.ultima_tabla:
            ui.notify("Primero genera la cotización.", color="warning")
            return
        try:
            pdf = generar_pdf_cotizacion(self.ultima_cotizacion, self.ultima_tabla)
            ui.download(pdf, self.ultima_cotizacion.id + "_autoventas.pdf")
        except Exception:
            ui.notify("No se pudo generar el PDF. Intenta nuevamente.", color="negative")

    @staticmethod
    def _buscar(datos, codigo):
        return next((item for item in datos if item.id == codigo), None)

    @staticmethod
    def _vehiculo_en_url():
        try:
            valor = ui.context.client.request.query_params.get("v")
            return valor.replace("-", "") if valor else None
        except Exception:
            return None


def cotizar():
    CotizacionPage().render()
