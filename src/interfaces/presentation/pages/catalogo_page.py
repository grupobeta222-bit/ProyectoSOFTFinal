from html import escape

from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.context import car_media, get_vehiculos, ui


class CatalogoPage:
    def render(self):
        nav("catalogo")
        self.vehiculos = [item for item in get_vehiculos() if item.activo]
        with ui.element("div").style("padding-top:100px;"):
            with ui.element("div").classes("av-section"):
                ui.html('<div class="av-tag">Inventario disponible</div>')
                ui.html('<h2 class="av-h2">Catálogo de vehículos</h2>')
                self._crear_filtros()
                self.grid = ui.element("div").classes("av-grid")
                self._renderizar()
        footer()

    def _crear_filtros(self):
        marcas = ["Todas"] + sorted({item.marca for item in self.vehiculos})
        anios = ["Todos"] + sorted({str(item.anio) for item in self.vehiculos})
        with ui.element("div").classes("av-search-bar"):
            self.busqueda = ui.input(
                placeholder="Buscar por marca o modelo...",
                on_change=self._renderizar,
            ).style("flex:1;min-width:210px;")
            self.marca = ui.select(marcas, value="Todas", label="Marca").style("min-width:130px;")
            self.anio = ui.select(anios, value="Todos", label="Año").style("min-width:120px;")
            self.precio = ui.number(
                label="Precio máximo", value=50000, min=0, step=1000
            ).style("min-width:150px;")
        self.marca.on("update:model-value", self._renderizar)
        self.anio.on("update:model-value", self._renderizar)
        self.precio.on("update:model-value", self._renderizar)

    def _renderizar(self, _evento=None):
        if not hasattr(self, "grid"):
            return
        encontrados = [item for item in self.vehiculos if self._coincide(item)]
        self.grid.clear()
        with self.grid:
            if not encontrados:
                ui.label("No se encontraron vehículos.").style("color:#777;")
                return
            for vehiculo in encontrados:
                self._mostrar_vehiculo(vehiculo)

    def _coincide(self, vehiculo):
        texto = (self.busqueda.value or "").strip().lower()
        coincide_texto = (
            texto in vehiculo.marca.lower()
            or texto in vehiculo.modelo.lower()
        )
        return (
            (self.marca.value == "Todas" or vehiculo.marca == self.marca.value)
            and (self.anio.value == "Todos" or str(vehiculo.anio) == str(self.anio.value))
            and (not self.precio.value or vehiculo.precio_base <= float(self.precio.value))
            and coincide_texto
        )

    def _mostrar_vehiculo(self, vehiculo):
        clase_stock = "low" if vehiculo.stock <= 3 else "ok"
        with ui.element("div").classes("av-card"):
            ui.html(car_media(vehiculo))
            with ui.element("div").classes("av-car-body"):
                ui.html(f'<div class="av-car-brand">{escape(vehiculo.marca)}</div>')
                ui.html(f'<div class="av-car-name">{escape(vehiculo.modelo)}</div>')
                ui.html(f'<div class="av-car-year">{vehiculo.anio} · {escape(vehiculo.combustible)}</div>')
                ui.html(f'<div class="av-car-price">${vehiculo.precio_base:,.0f} <small>precio base</small></div>')
                ui.html(f'''<div class="av-tags">
                  <span class="av-tag-chip">{escape(vehiculo.motor)}</span>
                  <span class="av-tag-chip">{escape(vehiculo.transmision)}</span>
                  <span class="av-tag-chip {clase_stock}">{vehiculo.stock} en stock</span>
                </div>''')
            with ui.element("div").classes("av-car-actions"):
                ui.button("Ver detalle", on_click=lambda codigo=vehiculo.id: ui.navigate.to("/vehiculo/" + codigo)).classes("av-btn-s")
                ui.button("Cotizar", on_click=lambda codigo=vehiculo.id: ui.navigate.to("/cotizar?v=" + codigo)).classes("av-btn-p")


def catalogo():
    CatalogoPage().render()
