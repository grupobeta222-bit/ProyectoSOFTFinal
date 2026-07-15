from src.interfaces.presentation.context import car_image_src, ui


def ir_cotizar(vehiculo_id):
    ui.navigate.to("/cotizar?v=" + vehiculo_id)


def boton_cotizar(vehiculo_id):
    def click():
        ir_cotizar(vehiculo_id)
    return click


def render_promo_carousel(vehiculos):
    slides = []
    for vehiculo in vehiculos[:3]:
        slides.append(vehiculo)

    if not slides:
        return

    with ui.element("div").style("background:#0f0f0f;padding:80px 0;"):
        with ui.element("div").classes("av-section"):
            ui.html('<div class="av-tag">Promociones</div>')
            ui.html('<h2 class="av-h2">Carrusel de promociones</h2>')
            ui.html('<p class="av-subsection-text">Modelos destacados para cotización rápida.</p>')

            with ui.carousel(animated=True, arrows=True, navigation=True).props(
                "height=360px autoplay"
            ).classes("w-full"):
                for vehiculo in slides:
                    with ui.carousel_slide().style(
                        "background:#141414;border:1px solid #242424;"
                        "border-radius:22px;padding:28px;"
                    ):
                        with ui.row().style(
                            "height:100%;align-items:center;"
                            "justify-content:space-between;gap:30px;"
                        ):
                            with ui.column().style("gap:10px;max-width:430px;"):
                                ui.html('<div class="av-eyebrow">Oferta destacada</div>')
                                ui.html(f'<div style="font-size:34px;font-weight:900;color:#fff;">{vehiculo.marca} {vehiculo.modelo}</div>')
                                ui.html(f'<div style="color:#888;font-size:14px;line-height:1.6;">Año {vehiculo.anio} · {vehiculo.motor} · {vehiculo.transmision} · {vehiculo.combustible}</div>')
                                ui.html(f'<div style="font-size:28px;font-weight:900;color:#e63946;margin-top:8px;">Desde ${vehiculo.precio_base:,.0f}</div>')
                                ui.button(
                                    "Cotizar promoción",
                                    on_click=boton_cotizar(vehiculo.id),
                                ).classes("av-btn-p").style(
                                    "width:max-content;margin-top:10px;"
                                )
                            ui.html(f'''
                            <img src="{car_image_src(vehiculo)}"
                                 alt="{vehiculo.marca} {vehiculo.modelo}"
                                 style="max-width:420px;width:45%;height:260px;
                                        object-fit:contain;
                                        filter:drop-shadow(0 25px 38px rgba(0,0,0,.45));">
                            ''')
