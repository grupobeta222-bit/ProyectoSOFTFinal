from html import escape

from src.interfaces.presentation.components.footer import footer
from src.interfaces.presentation.components.navigation import nav
from src.interfaces.presentation.context import (
    cerrar_sesion_cliente,
    guardar_sesion_cliente,
    login_cliente,
    registrar_cliente,
    ui,
)


class ClienteLoginPage:
    def render(self):
        nav("mi_cuenta")
        cerrar_sesion_cliente()
        with ui.element("div").style(
            "min-height:80vh;padding:100px 18px 40px;display:flex;flex-direction:column;"
            "justify-content:center;align-items:center;background:#0a0a0a;"
        ):
            with ui.tabs().classes("w-full max-w-md").style("margin-bottom:15px;") as tabs:
                ui.tab("Ingresar", icon="login")
                ui.tab("Registrarse", icon="person_add")
            with ui.tab_panels(tabs, value="Ingresar").classes("w-full max-w-md bg-transparent"):
                with ui.tab_panel("Ingresar"):
                    self._formulario_login()
                with ui.tab_panel("Registrarse"):
                    self._formulario_registro()
        footer()

    def _formulario_login(self):
        with self._card():
            ui.html('<h2 class="av-h2" style="font-size:24px;text-align:center;margin-bottom:20px;">Bienvenido de vuelta</h2>')
            correo = self._input("Correo electrónico")
            clave = self._input_clave("Contraseña")
            mensaje = ui.html("")
            ui.button(
                "Ingresar a mi cuenta",
                on_click=lambda: self._hacer_login(correo.value, clave.value, mensaje),
            ).classes("av-btn-p").style("width:100%;")

    def _formulario_registro(self):
        with self._card():
            ui.html('<h2 class="av-h2" style="font-size:24px;text-align:center;margin-bottom:20px;">Crear nueva cuenta</h2>')
            nombre = self._input("Nombre completo", "10px")
            correo = self._input("Correo electrónico", "10px")
            cedula = self._input("Cédula", "10px")
            telefono = self._input("Teléfono", "10px")
            clave = self._input_clave("Contraseña (mínimo 8 caracteres)")
            mensaje = ui.html("")
            ui.button(
                "Crear cuenta",
                on_click=lambda: self._hacer_registro(
                    nombre.value, correo.value, cedula.value,
                    telefono.value, clave.value, mensaje,
                ),
            ).classes("av-btn-p").style("width:100%;")

    def _hacer_login(self, correo, clave, mensaje):
        try:
            datos = login_cliente(correo, clave)
        except Exception:
            datos = None
        if not datos:
            self._mostrar_error(mensaje, "Correo o contraseña incorrectos.")
            return
        guardar_sesion_cliente(datos)
        ui.notify("Bienvenido", color="positive")
        ui.navigate.to("/mi-panel")

    def _hacer_registro(self, nombre, correo, cedula, telefono, clave, mensaje):
        try:
            registrar_cliente(nombre, correo, cedula, telefono, clave)
            datos = login_cliente(correo, clave)
            guardar_sesion_cliente(datos)
            ui.notify("Cuenta creada con éxito", color="positive")
            ui.navigate.to("/mi-panel")
        except Exception as error:
            self._mostrar_error(mensaje, str(error))

    @staticmethod
    def _card():
        return ui.element("div").style(
            "background:#121212;padding:30px;border-radius:12px;border:1px solid #333;"
            "box-shadow:0 10px 30px rgba(0,0,0,.5);"
        )

    @staticmethod
    def _input(label, margen="15px"):
        return ui.input(label=label).style(f"width:100%;margin-bottom:{margen};").props("outlined")

    @staticmethod
    def _input_clave(label):
        return ui.input(label=label, password=True, password_toggle_button=True).style(
            "width:100%;margin-bottom:20px;"
        ).props("outlined")

    @staticmethod
    def _mostrar_error(contenedor, mensaje):
        contenedor.set_content(
            '<div style="color:#ff4d4d;font-size:14px;margin-bottom:10px;">'
            + escape(mensaje) + "</div>"
        )


def cliente_login():
    ClienteLoginPage().render()
