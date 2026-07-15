from src.interfaces.presentation.context import (
    add_css,
    cliente_logueado,
    get_cliente_actual,
    get_cotizaciones_cliente,
    ui,
)


class Navigation:
    OPCIONES = [
        ("inicio", "Inicio", "/"),
        ("catalogo", "Vehículos", "/catalogo"),
        ("financiamiento", "Financiamiento", "/financiamiento"),
        ("cotizar", "Cotizar", "/cotizar"),
        ("asistente", "Asistente", "/asistente"),
        ("contacto", "Contacto", "/contacto"),
        ("mi_cuenta", "Mi cuenta", "/mi-panel"),
    ]

    def __init__(self, active):
        self.active = active

    def render(self):
        add_css()
        with ui.element("nav").classes("av-nav"):
            ui.html('<div class="av-logo">Auto<span>Ventas</span> Pro</div>').on(
                "click", lambda: ui.navigate.to("/")
            )
            with ui.element("div").classes("av-links"):
                self._links()
            with ui.element("div").classes("av-nav-actions"):
                if cliente_logueado():
                    self._campana()
                ui.button("Cotizar ahora", on_click=lambda: ui.navigate.to("/cotizar")).classes("av-cta av-desktop-cta")
                with ui.button(icon="menu").props("flat round color=white").classes("av-mobile-menu-btn"):
                    with ui.menu().classes("av-mobile-menu"):
                        for _key, label, ruta in self.OPCIONES:
                            ui.menu_item(label, on_click=lambda destino=ruta: ui.navigate.to(destino))

    def _links(self):
        for key, label, ruta in self.OPCIONES:
            clase = "av-link active" if key == self.active else "av-link"
            ui.link(label, ruta).classes(clase)

    def _cotizaciones_actualizadas(self):
        cliente = get_cliente_actual()
        cotizaciones = get_cotizaciones_cliente(cliente.get("email", ""))
        estados = {"en_revision", "aprobada", "rechazada", "cerrada"}
        return [item for item in cotizaciones if str(item.estado).lower() in estados]

    def _campana(self):
        nuevas = self._cotizaciones_actualizadas()
        with ui.button(icon="notifications").props("flat round color=white"):
            if nuevas:
                ui.badge(str(len(nuevas)), color="red").props("floating")
            with ui.menu().style("min-width:270px;padding:15px;border-radius:8px;"):
                if nuevas:
                    ui.label(f"Tienes {len(nuevas)} cotizaciones con actualizaciones.")
                    ui.button("Revisar cotizaciones", on_click=lambda: ui.navigate.to("/mi-panel")).classes("av-btn-p").style("width:100%;margin-top:10px;")
                else:
                    ui.label("No tienes actualizaciones.").style("color:#888;")


def nav(active="inicio"):
    Navigation(active).render()
