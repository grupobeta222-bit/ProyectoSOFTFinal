from html import escape

from src.interfaces.presentation.components.admin_layout import admin_shell, admin_title
from src.interfaces.presentation.context import (
    cambiar_estado_cotizacion_segura,
    es_gerente,
    get_cotizaciones,
    ui,
)
from src.interfaces.presentation.excel_reporte import generar_excel_cotizaciones
from src.interfaces.presentation.helpers import estado_normalizado, estado_texto, money
from src.interfaces.presentation.pdf_cotizacion import generar_pdf_cotizacion


class AdminCotizacionesPage:
    def __init__(self):
        self.cotizaciones = []

    def render(self):
        content = admin_shell("cotizaciones")
        if content is None:
            return
        self.cotizaciones = get_cotizaciones() or []
        with content:
            ui.html(admin_title("Cotizaciones registradas", "Control y seguimiento de cotizaciones."))
            ui.button("Exportar Excel", on_click=self.exportar_excel).classes(
                "av-btn-p"
            ).style("margin-bottom:18px;")
            with ui.card().style(
                "background:#141414;border:1px solid #242424;border-radius:22px;"
                "padding:26px;color:#fff;width:100%;"
            ):
                ui.html(f'''
                <div style="display:flex;justify-content:space-between;gap:14px;
                            align-items:center;margin-bottom:18px;flex-wrap:wrap;">
                  <h2 style="font-size:20px;color:#fff;margin:0;">
                    Listado de cotizaciones
                  </h2>
                  <span style="background:rgba(230,57,70,.12);
                               border:1px solid rgba(230,57,70,.45);color:#fff;
                               border-radius:999px;padding:8px 12px;font-size:12px;
                               font-weight:900;">
                    {len(self.cotizaciones)} registros
                  </span>
                </div>
                ''')
                if not self.cotizaciones:
                    ui.label("Todavía no hay cotizaciones registradas.").style("color:#aaa;")
                    return
                for cotizacion in self.cotizaciones:
                    self._mostrar_cotizacion(cotizacion)

    def exportar_excel(self):
        if not self.cotizaciones:
            ui.notify("No hay datos para exportar.", color="warning")
            return
        try:
            ui.download(
                generar_excel_cotizaciones(self.cotizaciones),
                "reporte_cotizaciones_autoventas.xlsx",
            )
        except Exception:
            ui.notify("No se pudo generar el archivo Excel.", color="negative")

    def _mostrar_cotizacion(self, cotizacion):
        estado = estado_normalizado(cotizacion.estado)
        with ui.element("div").style("width:100%;border-bottom:1px solid #252525;padding:16px 0;"):
            ui.html(f'''<div>
              <div style="font-weight:900;color:#fff;">{escape(cotizacion.id)} · {escape(cotizacion.nombre_cliente)}</div>
              <div style="font-size:12px;color:#888;margin-top:3px;">{escape(cotizacion.vehiculo_id)} · {escape(cotizacion.plan_id)} · {money(cotizacion.cuota_mensual)}</div>
              <span class="av-badge {estado}">{estado_texto(estado)}</span>
            </div>''')
            with ui.row().style("gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px;"):
                self._botones_estado(cotizacion, estado)
                ui.button("PDF", on_click=lambda item=cotizacion: self._exportar_pdf(item)).classes("av-btn-s")

    def _botones_estado(self, cotizacion, estado):
        if estado == "pendiente" and not es_gerente():
            self._boton_cambio("Enviar a revisión", cotizacion, "en_revision", "#e63946")
        elif estado == "en_revision" and es_gerente():
            self._boton_cambio("Aprobar", cotizacion, "aprobada", "#16a34a")
            self._boton_cambio("Rechazar", cotizacion, "rechazada", "#e63946")
        elif estado == "aprobada":
            self._boton_cambio("Cerrar venta", cotizacion, "cerrada", "#16a34a")
        elif estado == "pendiente":
            ui.label("Pendiente: el asesor debe enviarla a revisión").style("color:#ffd166;font-size:12px;")
        elif estado == "en_revision":
            ui.label("Esperando decisión del gerente").style("color:#a5b4fc;font-size:12px;")
        else:
            ui.label("Estado final registrado").style("color:#aaa;font-size:12px;")

    def _boton_cambio(self, texto, cotizacion, nuevo_estado, color):
        ui.button(
            texto,
            on_click=lambda item=cotizacion, estado=nuevo_estado: self._cambiar_estado(item, estado),
        ).style(
            f"background:{color};color:#fff;border-radius:10px;"
            "text-transform:none;font-weight:800;"
        )

    def _cambiar_estado(self, cotizacion, nuevo_estado):
        try:
            cambiar_estado_cotizacion_segura(cotizacion.id, nuevo_estado)
            ui.notify("Estado actualizado", color="positive")
            ui.navigate.to("/admin/cotizaciones")
        except Exception as error:
            ui.notify(str(error), color="negative")

    @staticmethod
    def _exportar_pdf(cotizacion):
        try:
            tabla = cotizacion.generar_tabla_amortizacion()
            ui.download(
                generar_pdf_cotizacion(cotizacion, tabla),
                cotizacion.id + "_autoventas.pdf",
            )
        except Exception:
            ui.notify("No se pudo generar el PDF.", color="negative")


def admin_cotizaciones():
    AdminCotizacionesPage().render()
