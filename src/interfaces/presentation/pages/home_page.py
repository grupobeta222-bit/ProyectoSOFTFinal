from html import escape

from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.components.promo_carousel import render_promo_carousel
from src.interfaces.presentation.context import car_media, get_testimonios, get_vehiculos, ui


class HomePage:
    def __init__(self):
        self.vehiculos = []
        self.testimonios = []

    def render(self):
        self.vehiculos = get_vehiculos()
        self.testimonios = get_testimonios()
        nav("inicio")
        self._hero()
        render_promo_carousel(self.vehiculos)
        self._beneficios()
        self._vehiculos_destacados()
        self._proceso_compra()
        self._seccion_testimonios()
        footer()

    def _hero(self):
        with ui.element("div").classes("av-hero"):
            with ui.element("div").classes("av-hero-layout"):
                with ui.element("div").classes("av-hero-inner"):
                    ui.html('<div class="av-eyebrow">Concesionaria Automotriz · Guayaquil, Ecuador</div>')
                    ui.html('<h1 class="av-h1">Encuentra el vehículo<br><em>ideal para ti</em></h1>')
                    ui.html('<p class="av-sub">Cotiza en minutos, conoce tu cuota mensual y da el primer paso hacia tu nuevo auto con nuestros planes de financiamiento.</p>')
                    with ui.element("div").classes("av-hero-btns"):
                        ui.button("Cotizar ahora", on_click=lambda: ui.navigate.to("/cotizar")).classes("av-btn-p")
                        ui.button("Ver vehículos", on_click=lambda: ui.navigate.to("/catalogo")).classes("av-btn-s")
                with ui.element("div").classes("av-hero-visual"):
                    ui.html('''<div class="av-hero-car-card">
                      <img class="av-hero-car-img" src="/assets/autos/veh001.jpg" alt="Vehículo destacado AutoVentas Pro">
                      <div class="av-hero-car-title">Toyota Corolla 2025</div>
                      <div class="av-hero-car-meta"><span class="av-hero-chip">Automática</span><span class="av-hero-chip">Gasolina</span><span class="av-hero-chip">5 en stock</span></div>
                      <div class="av-hero-price-row">
                        <div class="av-hero-price"><span>Desde</span>$25,990</div>
                        <div style="font-size:12px;color:#777;line-height:1.5;text-align:right;">
                          Entrada desde 20%<br>Plazos hasta 72 meses
                        </div>
                      </div>
                    </div>''')

    def _beneficios(self):
        with ui.element("div").style("background:#111;padding:80px 0;"):
            with ui.element("div").classes("av-section"):
                ui.html('<div class="av-tag">¿Por qué financiar con nosotros?</div>')
                ui.html('<h2 class="av-h2">Tus ventajas</h2>')
                ui.html('''<div class="av-benefits">
                  <div class="av-benefit">
                    <div class="av-benefit-icon">✔</div>
                    <div class="av-benefit-title">Planes flexibles</div>
                    <div class="av-benefit-desc">Desde 12 hasta 72 meses. Elige el plazo que mejor se adapte a tu presupuesto.</div>
                  </div>
                  <div class="av-benefit">
                    <div class="av-benefit-icon">⚡</div>
                    <div class="av-benefit-title">Respuesta rápida</div>
                    <div class="av-benefit-desc">Un asesor te contacta en menos de 24 horas tras enviar tu solicitud.</div>
                  </div>
                  <div class="av-benefit">
                    <div class="av-benefit-icon">👤</div>
                    <div class="av-benefit-title">Atención personalizada</div>
                    <div class="av-benefit-desc">Cada cliente tiene un asesor asignado durante todo el proceso.</div>
                  </div>
                  <div class="av-benefit">
                    <div class="av-benefit-icon">💰</div>
                    <div class="av-benefit-title">Tasas competitivas</div>
                    <div class="av-benefit-desc">Tasas desde el 8.5% anual. Transparencia total en cada cuota.</div>
                  </div>
                </div>''')

    def _vehiculos_destacados(self):
        with ui.element("div").style("background:#0f0f0f;padding:80px 0;"):
            with ui.element("div").classes("av-section"):
                ui.html('<div class="av-tag">Nuestros vehículos</div>')
                ui.html('<h2 class="av-h2">Vehículos destacados</h2>')
                with ui.element("div").classes("av-grid"):
                    for vehiculo in self.vehiculos[:4]:
                        self._tarjeta_vehiculo(vehiculo)
                ui.button(
                    "Ver todos los vehículos →",
                    on_click=lambda: ui.navigate.to("/catalogo"),
                ).classes("av-btn-s").style("display:block;margin:32px auto 0;")

    def _tarjeta_vehiculo(self, vehiculo):
        clase_stock = "low" if vehiculo.stock <= 3 else "ok"
        with ui.element("div").classes("av-card"):
            ui.html(car_media(vehiculo))
            with ui.element("div").classes("av-car-body"):
                ui.html(f'<div class="av-car-brand">{escape(vehiculo.marca)}</div>')
                ui.html(f'<div class="av-car-name">{escape(vehiculo.modelo)}</div>')
                ui.html(f'<div class="av-car-year">{vehiculo.anio}</div>')
                ui.html(f'<div class="av-car-price">${vehiculo.precio_base:,.0f} <small>precio base</small></div>')
                ui.html(f'''<div class="av-tags">
                  <span class="av-tag-chip">{escape(vehiculo.motor)}</span>
                  <span class="av-tag-chip">{escape(vehiculo.transmision)}</span>
                  <span class="av-tag-chip {clase_stock}">{vehiculo.stock} en stock</span>
                </div>''')
            with ui.element("div").classes("av-car-actions"):
                ui.button(
                    "Ver detalle",
                    on_click=lambda codigo=vehiculo.id: ui.navigate.to("/vehiculo/" + codigo),
                ).classes("av-btn-s")
                ui.button(
                    "Cotizar",
                    on_click=lambda codigo=vehiculo.id: ui.navigate.to("/cotizar?v=" + codigo),
                ).classes("av-btn-p")

    def _proceso_compra(self):
        with ui.element("div").style("background:#111;padding:80px 0;"):
            with ui.element("div").classes("av-section").style("text-align:center;"):
                ui.html('<div class="av-tag">¿Cómo funciona?</div>')
                ui.html('<h2 class="av-h2">Proceso de compra</h2>')
                ui.html('''<div class="av-steps-grid">
                  <a href="/catalogo" style="text-decoration:none;color:inherit;">
                    <div class="av-step">
                      <div class="av-step-num">1</div>
                      <div class="av-step-title">Selecciona tu vehículo</div>
                      <div class="av-step-desc">Explora el catálogo y elige el que más te gusta.</div>
                    </div>
                  </a>
                  <a href="/cotizar" style="text-decoration:none;color:inherit;">
                    <div class="av-step">
                      <div class="av-step-num">2</div>
                      <div class="av-step-title">Configura tu financiamiento</div>
                      <div class="av-step-desc">Ajusta la entrada y el plazo con nuestra calculadora.</div>
                    </div>
                  </a>
                  <a href="/cotizar" style="text-decoration:none;color:inherit;">
                    <div class="av-step">
                      <div class="av-step-num">3</div>
                      <div class="av-step-title">Recibe tu cotización</div>
                      <div class="av-step-desc">Cuota mensual, amortización y resumen completo.</div>
                    </div>
                  </a>
                  <a href="/contacto" style="text-decoration:none;color:inherit;">
                    <div class="av-step">
                      <div class="av-step-num">4</div>
                      <div class="av-step-title">Un asesor te contacta</div>
                      <div class="av-step-desc">El asesor asignado continúa el proceso comercial.</div>
                    </div>
                  </a>
                </div>''')

    def _seccion_testimonios(self):
        with ui.element("div").style("background:#0f0f0f;padding:80px 0;"):
            with ui.element("div").classes("av-section"):
                ui.html('<div class="av-tag">Comentarios de clientes</div>')
                ui.html('<h2 class="av-h2">Opiniones reales</h2>')
                ui.html('<p class="av-sub" style="max-width:760px;margin:0 auto 28px;text-align:center;">Ingresa a tu cuenta de cliente para compartir tu experiencia.</p>')
                self._mostrar_testimonios()
                with ui.element("div").classes("av-comment-box").style("text-align:center;padding:40px;"):
                    ui.html('<h3 style="margin:0 0 10px;color:#fff;font-size:22px;">¿Quieres dejar tu testimonio?</h3>')
                    ui.html('<p style="margin:0 0 20px;color:#aaa;font-size:14px;">Ingresa a tu cuenta para publicar un comentario.</p>')
                    ui.button("Ingresar a mi cuenta", on_click=lambda: ui.navigate.to("/ingreso")).classes("av-btn-p")

    def _mostrar_testimonios(self):
        contenido = '<div class="av-benefits">'
        for testimonio in self.testimonios:
            nombre = escape(testimonio.nombre)
            texto = escape(testimonio.texto)
            estrellas = "⭐" * max(1, min(5, int(testimonio.calificacion)))
            contenido += f'''<div class="av-benefit" style="text-align:center;">
              {self._avatar(testimonio)}
              <div class="av-benefit-title">{nombre}</div>
              <div style="color:#f59e0b;font-size:12px;margin-bottom:10px;">{estrellas}</div>
              <div class="av-benefit-desc" style="font-style:italic;">“{texto}”</div>
            </div>'''
        ui.html(contenido + "</div>")

    @staticmethod
    def _avatar(testimonio):
        nombre = escape(testimonio.nombre)
        if testimonio.foto_url:
            foto = escape(testimonio.foto_url, quote=True)
            return f'''
            <img src="{foto}" alt="{nombre}"
                 style="width:70px;height:70px;border-radius:50%;margin-bottom:15px;
                        border:3px solid #333;object-fit:cover;">
            '''
        return f'''
        <div style="width:70px;height:70px;border-radius:50%;margin:0 auto 15px;
                    background:#e63946;color:#fff;display:flex;align-items:center;
                    justify-content:center;font-weight:800;font-size:22px;
                    border:3px solid #333;">
          {escape(testimonio.iniciales)}
        </div>
        '''


def landing():
    HomePage().render()
