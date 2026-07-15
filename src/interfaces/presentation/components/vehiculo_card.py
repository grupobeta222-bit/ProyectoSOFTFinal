from src.interfaces.presentation.context import car_media, ui


def ir_detalle(vehiculo_id):
    ui.navigate.to("/vehiculo/" + vehiculo_id)


def ir_cotizar(vehiculo_id):
    ui.navigate.to("/cotizar?v=" + vehiculo_id)


def boton_detalle(vehiculo_id):
    def click():
        ir_detalle(vehiculo_id)
    return click


def boton_cotizar(vehiculo_id):
    def click():
        ir_cotizar(vehiculo_id)
    return click


def render_vehiculo_card(vehiculo, boton_texto="Cotizar"):
    stock = "ok"
    if vehiculo.stock <= 3:
        stock = "low"

    with ui.element("div").classes("av-card"):
        ui.html(car_media(vehiculo))
        with ui.element("div").classes("av-car-body"):
            ui.html(f'<div class="av-car-brand">{vehiculo.marca}</div>')
            ui.html(f'<div class="av-car-name">{vehiculo.modelo}</div>')
            ui.html(f'<div class="av-car-year">{vehiculo.anio} · {getattr(vehiculo, "combustible", "")}</div>')
            ui.html(f'<div class="av-car-price">${vehiculo.precio_base:,.0f} <small>precio base</small></div>')
            ui.html(f'''
            <div class="av-tags">
              <span class="av-tag-chip">{getattr(vehiculo, "motor", "N/D")}</span>
              <span class="av-tag-chip">{getattr(vehiculo, "transmision", "N/D")}</span>
              <span class="av-tag-chip {stock}">{vehiculo.stock} en stock</span>
            </div>
            ''')
        with ui.element("div").classes("av-car-actions"):
            ui.button("Ver detalle", on_click=boton_detalle(vehiculo.id)).classes("av-btn-s")
            ui.button(boton_texto, on_click=boton_cotizar(vehiculo.id)).classes("av-btn-p")
