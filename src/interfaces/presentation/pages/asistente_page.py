import html
import re

from nicegui import run

from src.interfaces.presentation.agente_cli import AgenteConversacional
from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.context import svc, ui


class AsistentePage:
    def __init__(self, service):
        self.agente = AgenteConversacional(service)
        self.chat_box = None
        self.entrada = None
        self.boton = None

    def render(self):
        nav("asistente")
        with ui.element("div").classes("av-asistente-page"):
            with ui.element("div").classes("av-asistente-card"):
                ui.html('<div class="av-tag">Asistente Virtual</div>')
                ui.html('<h2 class="av-h2" style="margin-bottom:14px;">Chatea con nuestro asesor IA</h2>')
                ui.html('<p style="font-size:14px;color:#777;margin-bottom:28px;line-height:1.65;">Consulta el catálogo, los planes y genera una cotización guiada.</p>')
                self.chat_box = ui.element("div").classes("av-chat-box")
                with self.chat_box:
                    ui.html('<div class="av-chat-bot">¡Hola! Soy el asistente de AutoVentas Pro. ¿Qué vehículo o plan deseas consultar?</div>')
                with ui.element("div").classes("av-chat-input-row"):
                    self.entrada = ui.input(placeholder="Ejemplo: quiero cotizar un Corolla").classes("av-chat-input").style("flex:1;")
                    self.boton = ui.button("Enviar", on_click=self.enviar).classes("av-btn-p").style("padding:12px 24px !important;")
                    self.entrada.on("keydown.enter", self.enviar)
        footer()

    async def enviar(self, _evento=None):
        texto = (self.entrada.value or "").strip()
        if not texto or not self.boton.enabled:
            return
        self.entrada.value = ""
        self.boton.disable()
        self.entrada.disable()
        self._agregar_mensaje(texto, "av-chat-user")
        espera = self._agregar_mensaje("Procesando tu consulta...", "av-chat-bot")
        try:
            respuesta = await run.io_bound(self.agente.procesar_entrada, texto)
            espera.delete()
            self._agregar_mensaje(self._respuesta_segura(str(respuesta)), "av-chat-bot", True)
        except Exception:
            espera.delete()
            self._agregar_mensaje("El asistente no está disponible en este momento. Intenta nuevamente.", "av-chat-bot")
        finally:
            self.boton.enable()
            self.entrada.enable()
            ui.run_javascript('const chat=document.querySelector(".av-chat-box");if(chat){chat.scrollTop=chat.scrollHeight;}')

    def _agregar_mensaje(self, texto, clase, es_html=False):
        contenido = texto if es_html else html.escape(str(texto)).replace("\n", "<br>")
        with self.chat_box:
            return ui.html(f'<div class="{clase}">{contenido}</div>')

    def _respuesta_segura(self, respuesta):
        self._enlaces_seguros = []
        patron = r'<a\s+href=["\'](/[^"\']*)["\'][^>]*>(.*?)</a>'
        texto = re.sub(patron, self._guardar_enlace, respuesta, flags=re.IGNORECASE | re.DOTALL)
        texto = html.escape(texto).replace("\n", "<br>")
        for indice, enlace in enumerate(self._enlaces_seguros):
            texto = texto.replace(f"__ENLACE_SEGURO_{indice}__", enlace)
        return texto

    def _guardar_enlace(self, coincidencia):
        ruta = coincidencia.group(1)
        etiqueta = html.escape(re.sub(r"<[^>]+>", "", coincidencia.group(2)))
        token = f"__ENLACE_SEGURO_{len(self._enlaces_seguros)}__"
        self._enlaces_seguros.append(f'<a href="{html.escape(ruta)}">{etiqueta}</a>')
        return token


def asistente():
    AsistentePage(svc).render()
