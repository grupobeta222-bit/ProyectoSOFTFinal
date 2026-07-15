from html import escape

from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.context import ASESORES, container, ui


class ContactoPage:
    def __init__(self, contacto_service, asesores):
        self.service = contacto_service
        self.asesores = asesores

    def render(self):
        nav("contacto")
        with ui.element("div").style("padding-top:100px;"):
            self._mostrar_contacto()
            self._mostrar_asesores()
            self._mostrar_preguntas()
        footer()

    def _mostrar_contacto(self):
        config = self.service.config
        whatsapp = escape(self.service.enlace_whatsapp(), quote=True)
        correo = escape(self.service.enlace_correo(), quote=True)
        with ui.element("div").classes("av-section"):
            ui.html('<div class="av-tag">Estamos aquí para ayudarte</div>')
            ui.html('<h2 class="av-h2">Contáctanos</h2>')
            ui.html(f'''<div class="av-contact-grid">
              <div class="av-contact-info">
                <div class="av-contact-item"><div class="av-contact-icon">📍</div><div class="av-contact-text"><h4>Dirección</h4><p>Av. Francisco de Orellana, Guayaquil, Ecuador</p></div></div>
                <div class="av-contact-item"><div class="av-contact-icon">💬</div><div class="av-contact-text"><h4>WhatsApp</h4><p>{config.whatsapp_visible}</p></div></div>
                <div class="av-contact-item"><div class="av-contact-icon">✉</div><div class="av-contact-text"><h4>Correo</h4><p>{config.email}</p></div></div>
                <div class="av-contact-item"><div class="av-contact-icon">🕐</div><div class="av-contact-text"><h4>Horario</h4><p>Lunes a sábado · 08:00 – 18:00</p></div></div>
              </div>
              <div class="av-cot-card">
                <div class="av-cot-step-title">Atención comercial</div>
                <p style="font-size:13px;color:#aaa;line-height:1.6;">Elige el canal que prefieras. Se abrirá WhatsApp o tu aplicación de correo.</p>
                <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px;">
                  <a class="av-btn-p" href="{whatsapp}" target="_blank" rel="noopener noreferrer">Abrir WhatsApp</a>
                  <a class="av-btn-s" href="{correo}">Enviar correo</a>
                </div>
              </div>
            </div>''')
            ui.button("Ir al cotizador", on_click=lambda: ui.navigate.to("/cotizar")).classes("av-btn-p").style("margin-top:24px;")

    def _mostrar_asesores(self):
        with ui.element("div").classes("av-section").style("padding-top:20px;"):
            ui.html('<div class="av-tag">Equipo comercial</div>')
            ui.html('<h2 class="av-h2">Nuestros asesores</h2>')
            with ui.element("div").classes("av-advisors-grid"):
                for asesor in self.asesores:
                    self._mostrar_asesor(asesor)

    def _mostrar_asesor(self, asesor):
        nombre = escape(asesor["nombre"])
        usuario = escape(asesor["usuario"])
        ui.html(f'''<div class="av-advisor-card">
          <div class="av-advisor-avatar">{nombre[0]}</div>
          <div class="av-advisor-name">{nombre}</div>
          <div class="av-advisor-text">Asesor comercial</div>
          <div class="av-advisor-text">{usuario}</div>
          <a class="av-advisor-link" href="/cotizar">Solicitar asesoría</a>
        </div>''')

    def _mostrar_preguntas(self):
        with ui.element("div").classes("av-section").style("padding-top:20px;"):
            ui.html('<div class="av-tag">Preguntas frecuentes</div>')
            ui.html('<h2 class="av-h2">Antes de cotizar</h2>')
            ui.html('''<div class="av-faq-grid">
              <div class="av-faq-card"><b>¿Puedo cotizar sin compromiso?</b><p>Sí. La cotización es referencial y no obliga a comprar.</p></div>
              <div class="av-faq-card"><b>¿Qué datos necesito?</b><p>Nombre, cédula, correo, teléfono, ciudad, entrada, vehículo y plan.</p></div>
              <div class="av-faq-card"><b>¿Me contactan después?</b><p>Sí. Un asesor puede ayudarte con disponibilidad y condiciones.</p></div>
            </div>''')


def contacto():
    ContactoPage(container.contacto_service, ASESORES).render()
