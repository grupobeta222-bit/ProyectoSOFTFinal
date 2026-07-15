from src.interfaces.presentation.context import ASESORES, car_image_src, get_vehiculos, ui
from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.components.vehiculo_card import render_vehiculo_card
from src.interfaces.presentation.helpers import money


def ir_catalogo():
    ui.navigate.to("/catalogo")


def ir_contacto():
    ui.navigate.to("/contacto")


def ir_cotizar(vehiculo_id):
    ui.navigate.to("/cotizar?v=" + vehiculo_id)


def boton_cotizar(vehiculo_id):
    def click():
        ir_cotizar(vehiculo_id)
    return click


def fila_info(label, value):
    return f'<div class="av-detail-info-row"><b>{label}</b><span>{value}</span></div>'


def buscar_vehiculo(vehiculos, vehiculo_id):
    for vehiculo in vehiculos:
        if vehiculo.id == vehiculo_id:
            return vehiculo
    return None


def asesor_por_vehiculo(vehiculo_id):
    try:
        numero = int(str(vehiculo_id).replace("VEH", ""))
        indice = (numero - 1) % len(ASESORES)
        return ASESORES[indice]
    except Exception:
        return ASESORES[0]


def otros_vehiculos(vehiculos, vehiculo_id):
    resultado = []
    for vehiculo in vehiculos:
        if vehiculo.id != vehiculo_id and len(resultado) < 3:
            resultado.append(vehiculo)
    return resultado


def bloque_detalle(vehiculo):
    estado = "Disponible"
    if vehiculo.stock <= 0:
        estado = "Sin stock"

    etiqueta_stock = "Disponible"
    if vehiculo.stock <= 3:
        etiqueta_stock = "Pocas unidades"

    ui.html(f'''
    <div class="av-detail-main">
      <div class="av-detail-photo-box">
        <img class="av-detail-main-img" src="{car_image_src(vehiculo)}" alt="{vehiculo.marca} {vehiculo.modelo}">
        <span class="av-photo-label">Imagen referencial</span>
        <span class="av-stock-label">{etiqueta_stock}</span>
      </div>
    </div>
    ''')

    with ui.row().classes("av-detail-actions"):
        ui.button("Solicitar más información", on_click=ir_contacto).classes("av-btn-s")
        ui.button("Cotizar este vehículo", on_click=boton_cotizar(vehiculo.id)).classes("av-btn-p")
        ui.button("Volver al catálogo", on_click=ir_catalogo).classes("av-btn-s")

    return estado


def bloque_informacion(vehiculo, estado):
    html = '<div class="av-detail-info"><h3 style="margin:0 0 12px;color:#18202c;font-size:18px;">Descripción</h3>'
    html += fila_info("Año", vehiculo.anio)
    html += fila_info("Marca", vehiculo.marca)
    html += fila_info("Modelo", vehiculo.modelo)
    html += fila_info("Condición", "Nuevo")
    html += fila_info("Motor", getattr(vehiculo, "motor", "N/D"))
    html += fila_info("Transmisión", getattr(vehiculo, "transmision", "N/D"))
    html += fila_info("Combustible", getattr(vehiculo, "combustible", "N/D"))
    html += fila_info("Stock", str(vehiculo.stock) + " unidades")
    html += fila_info("Estado", estado)
    html += fila_info("Código", vehiculo.id)
    html += '</div>'
    ui.html(html)


def bloque_asesor(asesor):
    ui.html(f'''
    <div class="av-advisor-card-light">
      <div class="av-advisor-label">Asesor disponible</div>
      <div class="av-advisor-name">{asesor["nombre"]}</div>
      <div class="av-advisor-text">{asesor["usuario"]}</div>
      <div class="av-advisor-text">Teléfono: 099-000-000{asesor["id"]}</div>
    </div>
    ''')


def vehiculo_detalle(vehiculo_id: str):
    nav("catalogo")
    vehiculos = get_vehiculos() or []
    vehiculo = buscar_vehiculo(vehiculos, vehiculo_id)

    with ui.element("div").classes("av-detail-wrap"):
        with ui.element("div").classes("av-section"):
            if vehiculo is None:
                ui.html('<div class="av-alert-err">No se encontró el vehículo solicitado.</div>')
                ui.button("Volver al catálogo", on_click=ir_catalogo).classes("av-btn-p")
                footer()
                return

            asesor = asesor_por_vehiculo(vehiculo.id)
            ui.html('<div class="av-tag">Detalle del vehículo</div>')
            ui.html(f'<h2 class="av-h2">{vehiculo.marca} {vehiculo.modelo}</h2>')

            with ui.element("div").classes("av-detail-grid"):
                with ui.element("div"):
                    estado = bloque_detalle(vehiculo)

                with ui.element("div").classes("av-detail-side"):
                    ui.html(f'<div class="av-detail-title">{vehiculo.anio} {vehiculo.marca} {vehiculo.modelo}</div>')
                    ui.html(f'<div class="av-detail-meta">{vehiculo.anio} · {vehiculo.marca} · {vehiculo.modelo}</div>')
                    ui.html(f'<div class="av-detail-price">{money(vehiculo.precio_base)}</div>')
                    ui.html('<div class="av-detail-note">Precio y disponibilidad sujetos a confirmación.</div>')
                    bloque_informacion(vehiculo, estado)
                    bloque_asesor(asesor)

            relacionados = otros_vehiculos(vehiculos, vehiculo.id)
            if relacionados:
                ui.html('<h2 class="av-h2" style="margin-top:46px;font-size:28px;">Explora otros vehículos</h2>')
                with ui.element("div").classes("av-grid"):
                    for vehiculo_relacionado in relacionados:
                        render_vehiculo_card(vehiculo_relacionado, "Cotizar")
    footer()
