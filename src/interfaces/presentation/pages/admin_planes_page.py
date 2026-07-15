from html import escape

from src.interfaces.presentation.components.admin_layout import admin_shell, admin_title
from src.interfaces.presentation.context import es_gerente, get_planes, svc, ui
from src.interfaces.presentation.helpers import money


class AdminPlanesPage:
    def render(self):
        content = admin_shell("planes")
        if content is None:
            return
        with content:
            if not es_gerente():
                ui.html(admin_title("Planes de financiamiento", "Esta sección solo está disponible para el gerente."))
                return
            ui.html(admin_title("Gestión de planes de financiamiento", "Tasas, entrada mínima, plazos y comisiones."))
            planes = get_planes()
            if not planes:
                ui.label("Todavía no hay planes registrados.").style("color:#aaa;")
                return
            with ui.element("section").style("display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;"):
                for plan in planes:
                    self._mostrar_plan(plan)
            ui.html('<style>@media(max-width:1100px){section{grid-template-columns:1fr!important;}}</style>')

    def _mostrar_plan(self, plan):
        estado = "Activo" if plan.activo else "Inactivo"
        with ui.card().style(
            "background:#141414;border:1px solid #242424;border-radius:22px;"
            "padding:22px;color:#fff;"
        ):
            ui.html(f'<div style="font-size:12px;color:#e63946;font-weight:900;">{escape(plan.id)} · {estado}</div>')
            ui.html(f'<h2 style="font-size:24px;color:#fff;margin:7px 0 16px;">{escape(plan.nombre)}</h2>')
            plazos = ", ".join(str(item) for item in plan.plazos_disponibles)
            ui.html(f'''<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-bottom:18px;">
              <div style="background:#1b1b1b;border-radius:14px;padding:14px;">
                <div style="color:#777;font-size:12px;">Entrada mínima</div>
                <div style="font-size:22px;font-weight:900;">{plan.entrada_minima_porcentaje}%</div>
              </div>
              <div style="background:#1b1b1b;border-radius:14px;padding:14px;">
                <div style="color:#777;font-size:12px;">Tasa anual</div>
                <div style="font-size:22px;font-weight:900;">{plan.tasa_anual}%</div>
              </div>
              <div style="background:#1b1b1b;border-radius:14px;padding:14px;">
                <div style="color:#777;font-size:12px;">Plazos</div>
                <div style="font-weight:900;">{plazos} meses</div>
              </div>
              <div style="background:#1b1b1b;border-radius:14px;padding:14px;">
                <div style="color:#777;font-size:12px;">Comisión</div>
                <div style="font-size:22px;font-weight:900;">{money(plan.comision_apertura)}</div>
              </div>
            </div>''')
            ui.button("Editar plan", on_click=lambda item=plan: self._editar(item)).classes("av-btn-s")

    def _editar(self, plan):
        self.dialogo = ui.dialog()
        with self.dialogo, ui.card().style("background:#141414;color:#fff;min-width:420px;border:1px solid #333;border-radius:18px;"):
            ui.label("Editar plan").style("font-size:20px;font-weight:900;")
            self.plan_actual = plan
            self.nombre = ui.input("Nombre", value=plan.nombre).style("width:100%;")
            self.entrada = ui.number("Entrada mínima (%)", value=float(plan.entrada_minima_porcentaje)).style("width:100%;")
            self.tasa = ui.number("Tasa anual (%)", value=float(plan.tasa_anual)).style("width:100%;")
            self.plazos = ui.input("Plazos separados por coma", value=", ".join(str(item) for item in plan.plazos_disponibles)).style("width:100%;")
            self.comision = ui.number("Comisión", value=float(plan.comision_apertura)).style("width:100%;")
            self.mensaje = ui.html("")
            with ui.row().style("gap:10px;margin-top:12px;"):
                ui.button("Guardar", on_click=self._guardar).classes("av-btn-p")
                ui.button("Cancelar", on_click=self.dialogo.close).classes("av-btn-s")
        self.dialogo.open()

    def _guardar(self):
        try:
            plazos = [int(item.strip()) for item in (self.plazos.value or "").split(",") if item.strip()]
            svc.actualizar_plan(
                self.plan_actual.id, self.nombre.value, self.entrada.value,
                self.tasa.value, plazos, self.comision.value,
                activo=self.plan_actual.activo,
            )
            self.dialogo.close()
            ui.notify("Plan actualizado", color="positive")
            ui.navigate.to("/admin/planes")
        except Exception as error:
            self.mensaje.set_content(f'<div style="color:#ff9aa3;">{escape(str(error))}</div>')


def admin_planes():
    AdminPlanesPage().render()
