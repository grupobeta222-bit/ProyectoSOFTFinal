from html import escape

from src.interfaces.presentation.components.admin_layout import admin_shell, admin_title
from src.interfaces.presentation.context import es_gerente, get_vehiculos, svc, ui
from src.interfaces.presentation.helpers import money


class AdminVehiculosPage:
    def render(self):
        content = admin_shell("vehiculos")
        if content is None:
            return
        with content:
            if not es_gerente():
                ui.html(admin_title("Gestión de vehículos", "Esta sección solo está disponible para el gerente."))
                return
            ui.html(admin_title("Gestión de vehículos", "Catálogo, disponibilidad y datos principales."))
            vehiculos = get_vehiculos()
            with ui.element("section").style("display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;"):
                for vehiculo in vehiculos:
                    self._mostrar(vehiculo)
            ui.html('<style>@media(max-width:1100px){section{grid-template-columns:1fr!important;}}</style>')

    def _mostrar(self, vehiculo):
        estado = "Activo" if vehiculo.activo else "Inactivo"
        with ui.card().style("background:#141414;border:1px solid #242424;border-radius:22px;padding:22px;color:#fff;"):
            ui.html(f'''<div style="font-size:12px;color:#e63946;font-weight:900;">{escape(vehiculo.marca)} · {estado}</div>
              <h3 style="font-size:21px;color:#fff;margin:5px 0;">{escape(vehiculo.modelo)} {vehiculo.anio}</h3>
              <div style="font-size:24px;font-weight:900;margin:12px 0;">{money(vehiculo.precio_base)}</div>
              <div style="color:#aaa;margin-bottom:16px;">Stock: {vehiculo.stock} · {escape(vehiculo.transmision)} · {escape(vehiculo.combustible)}</div>''')
            with ui.row().style("gap:8px;flex-wrap:wrap;"):
                ui.button("Editar", on_click=lambda item=vehiculo: self._editar(item)).classes("av-btn-s")
                if vehiculo.activo:
                    ui.button("Desactivar", on_click=lambda item=vehiculo: self._desactivar(item)).classes("av-btn-p")

    def _editar(self, vehiculo):
        self.dialogo = ui.dialog()
        self.vehiculo_actual = vehiculo
        with self.dialogo, ui.card().style("background:#141414;color:#fff;min-width:430px;border:1px solid #333;border-radius:18px;"):
            ui.label("Editar vehículo").style("font-size:20px;font-weight:900;")
            self.marca = ui.input("Marca", value=vehiculo.marca).style("width:100%;")
            self.modelo = ui.input("Modelo", value=vehiculo.modelo).style("width:100%;")
            self.anio = ui.number("Año", value=vehiculo.anio).style("width:100%;")
            self.precio = ui.number("Precio base", value=float(vehiculo.precio_base)).style("width:100%;")
            self.stock = ui.number("Stock", value=vehiculo.stock).style("width:100%;")
            self.motor = ui.input("Motor", value=vehiculo.motor).style("width:100%;")
            self.transmision = ui.input("Transmisión", value=vehiculo.transmision).style("width:100%;")
            self.combustible = ui.input("Combustible", value=vehiculo.combustible).style("width:100%;")
            self.mensaje = ui.html("")
            with ui.row().style("gap:10px;margin-top:12px;"):
                ui.button("Guardar", on_click=self._guardar).classes("av-btn-p")
                ui.button("Cancelar", on_click=self.dialogo.close).classes("av-btn-s")
        self.dialogo.open()

    def _guardar(self):
        try:
            item = self.vehiculo_actual
            svc.actualizar_vehiculo(
                item.id, self.marca.value, self.modelo.value, self.anio.value,
                self.precio.value, self.stock.value, self.motor.value,
                self.transmision.value, self.combustible.value, item.activo,
            )
            self.dialogo.close()
            ui.notify("Vehículo actualizado", color="positive")
            ui.navigate.to("/admin/vehiculos")
        except Exception as error:
            self.mensaje.set_content(f'<div style="color:#ff9aa3;">{escape(str(error))}</div>')

    @staticmethod
    def _desactivar(vehiculo):
        try:
            svc.desactivar_vehiculo(vehiculo.id)
            ui.notify("Vehículo desactivado", color="positive")
            ui.navigate.to("/admin/vehiculos")
        except Exception as error:
            ui.notify(str(error), color="negative")


def admin_vehiculos():
    AdminVehiculosPage().render()
