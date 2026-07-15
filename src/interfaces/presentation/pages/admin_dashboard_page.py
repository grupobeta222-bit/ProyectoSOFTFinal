from html import escape

from src.interfaces.presentation.components.admin_layout import admin_shell, admin_title, card
from src.interfaces.presentation.context import (
    ASESORES,
    container,
    es_gerente,
    get_clientes,
    get_cotizaciones,
    get_planes,
    get_vehiculos,
    ui,
    usuario_actual,
)
from src.interfaces.presentation.excel_reporte import generar_excel_reporte
from src.interfaces.presentation.helpers import estado_texto, money
from src.interfaces.presentation.pdf_reporte import generar_pdf_reporte


class AdminDashboardPage:
    def __init__(self):
        self.cotizaciones = []
        self.vehiculos = []
        self.planes = []
        self.clientes = []
        self.filtradas = []
        self.panel = None

    def render(self):
        content = admin_shell("dashboard")
        if content is None:
            return
        self.cotizaciones = get_cotizaciones()
        self.vehiculos = get_vehiculos()
        self.planes = get_planes()
        self.clientes = get_clientes()

        with content:
            usuario = usuario_actual()
            titulo = "Dashboard gerencial" if es_gerente() else "Mi portal de asesor"
            subtitulo = "Indicadores de cotizaciones y ventas cerradas."
            ui.html(admin_title(titulo, subtitulo))
            self._filtros()
            self.panel = ui.element("div").style("width:100%;")
            self._actualizar_panel()

    def _filtros(self):
        marcas = ["Todas"] + sorted({item.marca for item in self.vehiculos})
        planes = {"Todos": "Todos los planes"}
        planes.update({item.id: item.nombre for item in self.planes})
        asesores = {"Todos": "Todos los asesores"}
        asesores.update({str(item["id"]): item["nombre"] for item in ASESORES})

        with ui.card().style(
            "width:100%;background:#141414;border:1px solid #242424;"
            "border-radius:18px;padding:18px;margin-bottom:20px;"
        ):
            with ui.row().style("width:100%;gap:12px;align-items:end;flex-wrap:wrap;"):
                self.desde = ui.input("Desde").props("type=date outlined").style("min-width:150px;")
                self.hasta = ui.input("Hasta").props("type=date outlined").style("min-width:150px;")
                self.marca = ui.select(marcas, value="Todas", label="Marca").props("outlined").style("min-width:150px;")
                self.plan = ui.select(planes, value="Todos", label="Plan").props("outlined").style("min-width:180px;")
                self.asesor = ui.select(asesores, value="Todos", label="Asesor").props("outlined").style("min-width:190px;")
                if not es_gerente():
                    self.asesor.set_visibility(False)
                ui.button("Aplicar", on_click=self._actualizar_panel).classes("av-btn-p")

    def _actualizar_panel(self):
        self.filtradas = [item for item in self.cotizaciones if self._cumple_filtros(item)]
        resumen = container.dashboard_service.resumen(self.filtradas)
        ranking = container.dashboard_service.ranking(self.filtradas)
        self.panel.clear()
        with self.panel:
            self._kpis(resumen)
            with ui.row().style("width:100%;gap:20px;align-items:stretch;flex-wrap:wrap;"):
                self._estados(resumen)
                if es_gerente():
                    self._ranking(ranking)
            self._tabla()
            if es_gerente():
                with ui.row().style("gap:12px;margin-top:18px;flex-wrap:wrap;"):
                    ui.button("Exportar PDF", on_click=self._exportar_pdf).classes("av-btn-s")
                    ui.button("Exportar Excel", on_click=self._exportar_excel).classes("av-btn-p")

    def _cumple_filtros(self, cotizacion):
        fecha = str(cotizacion.fecha)[:10]
        vehiculo = next((item for item in self.vehiculos if item.id == cotizacion.vehiculo_id), None)
        if self.desde.value and fecha < self.desde.value:
            return False
        if self.hasta.value and fecha > self.hasta.value:
            return False
        if self.marca.value != "Todas" and (vehiculo is None or vehiculo.marca != self.marca.value):
            return False
        if self.plan.value != "Todos" and cotizacion.plan_id != self.plan.value:
            return False
        if es_gerente() and self.asesor.value != "Todos" and cotizacion.asesor_id != int(self.asesor.value):
            return False
        return True

    def _kpis(self, resumen):
        tasa = round(resumen["cerradas"] * 100 / resumen["total"], 1) if resumen["total"] else 0
        ui.html(f'''<section class="av-kpi-grid" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-bottom:26px;">
          {card('Cotizaciones', str(resumen['total']), '📄')}
          {card('Ventas cerradas', str(resumen['cerradas']), '✅')}
          {card('Tasa de cierre', str(tasa) + '%', '📈')}
          {card('Ingreso por ventas', money(resumen['ingresos']), '💰')}
        </section>''')

    def _estados(self, resumen):
        with ui.card().style("flex:1;min-width:300px;background:#141414;border:1px solid #242424;border-radius:18px;padding:22px;color:#fff;"):
            ui.label("Estado de cotizaciones").style("font-size:18px;font-weight:900;")
            datos = [
                ("Pendientes", resumen["pendientes"]),
                ("En revisión", resumen["en_revision"]),
                ("Aprobadas", resumen["aprobadas"]),
                ("Rechazadas", resumen["rechazadas"]),
                ("Cerradas", resumen["cerradas"]),
            ]
            for nombre, cantidad in datos:
                with ui.row().style("width:100%;justify-content:space-between;border-bottom:1px solid #262626;padding:9px 0;"):
                    ui.label(nombre)
                    ui.label(str(cantidad)).style("font-weight:900;color:#e63946;")

    def _ranking(self, ranking):
        with ui.card().style("flex:1.3;min-width:360px;background:#141414;border:1px solid #242424;border-radius:18px;padding:22px;color:#fff;"):
            ui.label("Ranking de asesores").style("font-size:18px;font-weight:900;")
            filas = "".join(
                f"<tr><td>{escape(item['nombre'])}</td><td>{item['cotizaciones']}</td>"
                f"<td>{item['cerradas']}</td><td>{money(item['valor'])}</td></tr>"
                for item in ranking
            )
            ui.html(f'''<div style="overflow-x:auto;"><table class="av-admin-table">
              <thead><tr><th>Asesor</th><th>Cotizaciones</th><th>Cerradas</th><th>Ingreso</th></tr></thead>
              <tbody>{filas}</tbody></table></div>''')

    def _tabla(self):
        filas = ""
        for item in self.filtradas[:20]:
            asesor = next((dato["nombre"] for dato in ASESORES if dato["id"] == item.asesor_id), "Sin asesor")
            filas += (
                f"<tr><td>{escape(item.id)}</td><td>{escape(item.nombre_cliente)}</td>"
                f"<td>{escape(asesor)}</td><td>{money(item.precio_vehiculo)}</td>"
                f"<td>{escape(estado_texto(item.estado))}</td></tr>"
            )
        if not filas:
            filas = '<tr><td colspan="5">No hay datos para los filtros seleccionados.</td></tr>'
        ui.html(f'''<div style="margin-top:20px;overflow-x:auto;background:#141414;border:1px solid #242424;border-radius:18px;padding:18px;">
          <table class="av-admin-table"><thead><tr><th>ID</th><th>Cliente</th><th>Asesor</th><th>Precio vehículo</th><th>Estado</th></tr></thead><tbody>{filas}</tbody></table>
        </div>''')

    def _exportar_pdf(self):
        try:
            ranking = container.dashboard_service.ranking(self.filtradas)
            ui.download(generar_pdf_reporte(self.filtradas, ranking, self._texto_filtros()), "reporte_gerencial.pdf")
        except Exception:
            ui.notify("No se pudo generar el PDF.", color="negative")

    def _exportar_excel(self):
        try:
            ranking = container.dashboard_service.ranking(self.filtradas)
            ui.download(
                generar_excel_reporte(
                    self.filtradas, ranking, self._texto_filtros(),
                    self._resumen_por("marca"), self._resumen_por("plan"),
                ),
                "reporte_gerencial.xlsx",
            )
        except Exception:
            ui.notify("No se pudo generar el Excel.", color="negative")

    def _resumen_por(self, tipo):
        conteo = {}
        for cotizacion in self.filtradas:
            if tipo == "marca":
                vehiculo = next((item for item in self.vehiculos if item.id == cotizacion.vehiculo_id), None)
                nombre = vehiculo.marca if vehiculo else "Sin marca"
            else:
                plan = next((item for item in self.planes if item.id == cotizacion.plan_id), None)
                nombre = plan.nombre if plan else "Sin plan"
            conteo[nombre] = conteo.get(nombre, 0) + 1
        return sorted(conteo.items())

    def _texto_filtros(self):
        return f"Desde {self.desde.value or 'inicio'} hasta {self.hasta.value or 'hoy'}; marca {self.marca.value}; plan {self.plan.value}."


def admin_dashboard():
    AdminDashboardPage().render()
