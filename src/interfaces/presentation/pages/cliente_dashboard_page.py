from html import escape

from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.context import (
    actualizar_cliente_perfil,
    cerrar_sesion_cliente,
    cliente_logueado,
    get_cliente_actual,
    get_cotizaciones_cliente,
    guardar_sesion_cliente,
    publicar_testimonio,
    ui,
)
from src.interfaces.presentation.helpers import estado_normalizado, estado_texto, money


class ClienteDashboardPage:
    COLORES = {
        "pendiente": "#f59e0b",
        "en_revision": "#3b82f6",
        "aprobada": "#10b981",
        "rechazada": "#ef4444",
        "cerrada": "#10b981",
    }

    def render(self):
        if not cliente_logueado():
            ui.navigate.to("/ingreso")
            return
        nav("mi_cuenta")
        self.cliente = get_cliente_actual()
        with ui.element("div").style("padding:100px 20px 40px;min-height:80vh;background:#0a0a0a;display:flex;justify-content:center;"):
            with ui.element("div").classes("av-client-layout"):
                tabs = self._sidebar()
                with ui.tab_panels(tabs, value="Mis cotizaciones").classes("w-full bg-transparent").style("padding:0;"):
                    with ui.tab_panel("Mis cotizaciones").style("padding:0;"):
                        self._panel_cotizaciones()
                    with ui.tab_panel("Mi experiencia").style("padding:0;"):
                        self._panel_resena()
                    with ui.tab_panel("Editar perfil").style("padding:0;"):
                        self._panel_perfil()
        footer()

    def _sidebar(self):
        nombre = self.cliente.get("nombre", "Cliente")
        with ui.element("div").style(
            "background:#121212;border:1px solid #333;border-radius:12px;"
            "padding:20px;display:flex;flex-direction:column;gap:10px;"
        ):
            ui.html(f'''<div style="text-align:center;margin-bottom:20px;">
              <div style="width:80px;height:80px;background:#e63946;border-radius:50%;
                          margin:0 auto 10px;display:flex;align-items:center;
                          justify-content:center;font-size:32px;font-weight:bold;color:#fff;">
                {escape(nombre[0].upper())}
              </div>
              <div style="font-weight:bold;font-size:18px;">{escape(nombre)}</div>
              <div style="color:#888;font-size:12px;word-break:break-all;">{escape(self.cliente.get('email', ''))}</div>
            </div>''')
            with ui.tabs().props("vertical").classes("w-full") as tabs:
                ui.tab("Mis cotizaciones", icon="receipt_long")
                ui.tab("Mi experiencia", icon="star_rate")
                ui.tab("Editar perfil", icon="manage_accounts")
            ui.button("Cerrar sesión", on_click=self._cerrar_sesion).classes("av-btn-s").style("width:100%;")
        return tabs

    def _panel_cotizaciones(self):
        ui.html('<h2 class="av-h2" style="margin-bottom:20px;">Historial de cotizaciones</h2>')
        cotizaciones = get_cotizaciones_cliente(self.cliente.get("email", ""))
        if not cotizaciones:
            with ui.element("div").style("background:#121212;padding:40px;border-radius:12px;text-align:center;border:1px dashed #444;"):
                ui.label("Aún no tienes cotizaciones activas.").style("color:#888;")
                ui.button("Ir al catálogo", on_click=lambda: ui.navigate.to("/catalogo")).classes("av-btn-p").style("margin-top:15px;")
            return
        with ui.element("div").classes("av-client-quotes"):
            for cotizacion in cotizaciones:
                self._tarjeta_cotizacion(cotizacion)

    def _tarjeta_cotizacion(self, cotizacion):
        estado = estado_normalizado(cotizacion.estado)
        color = self.COLORES.get(estado, "#888")
        with ui.element("div").style("background:#121212;padding:20px;border-radius:12px;border:1px solid #333;"):
            ui.html(f'''<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:10px;">
              <span style="font-weight:bold;font-size:18px;">{escape(cotizacion.id)}</span>
              <span style="background:{color};color:#fff;padding:3px 8px;border-radius:10px;font-size:11px;font-weight:bold;">{estado_texto(estado)}</span>
            </div>
            <div style="color:#aaa;font-size:14px;margin-bottom:5px;">Vehículo: {escape(cotizacion.vehiculo_id)}</div>
            <div style="color:#aaa;font-size:14px;">Cuota mensual: {money(cotizacion.cuota_mensual)}</div>''')
            if estado == "en_revision":
                ui.label("Un asesor está revisando tu caso.").style("color:#93c5fd;margin-top:10px;")
            elif estado == "aprobada":
                ui.label("La cotización fue aprobada y está pendiente de cierre.").style("color:#6ee7b7;margin-top:10px;")
            elif estado == "cerrada":
                ui.label("La venta fue cerrada.").style("color:#6ee7b7;margin-top:10px;")

    def _panel_resena(self):
        with ui.element("div").style("background:#121212;padding:30px;border-radius:12px;border:1px solid #333;max-width:600px;"):
            ui.label("Déjanos tu reseña").style("font-size:20px;font-weight:900;")
            self.comentario = ui.textarea(label="Tu comentario").props("outlined").style("width:100%;margin:15px 0;")
            self.calificacion = ui.select(
                {5: "⭐⭐⭐⭐⭐ Excelente", 4: "⭐⭐⭐⭐ Bueno", 3: "⭐⭐⭐ Regular"},
                label="Calificación", value=5,
            ).style("width:100%;margin-bottom:20px;")
            self.mensaje_resena = ui.html("")
            ui.button("Publicar comentario", on_click=self._publicar_resena).classes("av-btn-p").style("width:100%;")

    def _publicar_resena(self):
        try:
            publicar_testimonio(
                self.cliente.get("nombre"), self.cliente.get("email"),
                self.comentario.value, calificacion=self.calificacion.value,
            )
            self.comentario.value = ""
            self.mensaje_resena.set_content('<div style="color:#10b981;">Gracias. Tu comentario fue publicado.</div>')
        except Exception as error:
            self.mensaje_resena.set_content(f'<div style="color:#ef4444;">{escape(str(error))}</div>')

    def _panel_perfil(self):
        with ui.element("div").style("background:#121212;padding:30px;border-radius:12px;border:1px solid #333;max-width:600px;"):
            ui.label("Actualizar mis datos").style("font-size:20px;font-weight:900;")
            self.nombre = ui.input("Nombre", value=self.cliente.get("nombre")).props("outlined").style("width:100%;margin:15px 0;")
            self.cedula = ui.input("Cédula", value=self.cliente.get("cedula")).props("outlined").style("width:100%;margin-bottom:15px;")
            self.telefono = ui.input("Teléfono", value=self.cliente.get("telefono")).props("outlined").style("width:100%;margin-bottom:15px;")
            self.clave = ui.input("Nueva contraseña (opcional)", password=True, password_toggle_button=True).props("outlined").style("width:100%;margin-bottom:20px;")
            self.mensaje_perfil = ui.html("")
            ui.button("Guardar cambios", on_click=self._guardar_perfil).classes("av-btn-p").style("width:100%;")

    def _guardar_perfil(self):
        try:
            datos = actualizar_cliente_perfil(
                self.cliente.get("email"), self.nombre.value,
                self.telefono.value, self.cedula.value, self.clave.value,
            )
            guardar_sesion_cliente(datos)
            self.cliente = datos
            self.mensaje_perfil.set_content('<div style="color:#10b981;">Perfil actualizado.</div>')
        except Exception as error:
            self.mensaje_perfil.set_content(f'<div style="color:#ef4444;">{escape(str(error))}</div>')

    @staticmethod
    def _cerrar_sesion():
        cerrar_sesion_cliente()
        ui.navigate.to("/")


def cliente_dashboard():
    ClienteDashboardPage().render()
