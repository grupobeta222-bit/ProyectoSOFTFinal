from src.interfaces.presentation.context import (
    add_css,
    cerrar_sesion_admin,
    guardar_sesion,
    login_usuario,
    ui,
)


class LoginPage:
    def render(self):
        add_css()
        cerrar_sesion_admin()
        self._fondo()
        with ui.column().style(
            "min-height:100vh;width:100%;display:flex;align-items:center;"
            "justify-content:center;padding:96px 24px;"
        ):
            with ui.column().style(
                "width:100%;max-width:480px;background:rgba(18,18,18,.96);"
                "border:1px solid rgba(230,57,70,.34);border-radius:28px;"
                "padding:42px 36px;box-shadow:0 35px 110px rgba(0,0,0,.55);"
            ):
                self._encabezado()
                usuario = ui.input(
                    label="Correo", placeholder="usuario@autoventas.com"
                ).style("width:100%;margin-bottom:12px;")
                clave = ui.input(
                    label="Contraseña", password=True, password_toggle_button=True
                ).style("width:100%;margin-bottom:16px;")
                mensaje = ui.html("")
                ui.button(
                    "Ingresar",
                    on_click=lambda: self._ingresar(usuario.value, clave.value, mensaje),
                ).style(
                    "width:100%;background:#e63946;color:#fff;border-radius:14px;"
                    "padding:14px;font-size:15px;font-weight:900;text-transform:none;"
                )
                ui.button(
                    "Volver al inicio", on_click=lambda: ui.navigate.to("/")
                ).style(
                    "width:100%;margin-top:12px;background:#181818;color:#ccc;"
                    "border:1px solid #333;border-radius:14px;padding:12px;"
                    "font-size:13px;font-weight:800;text-transform:none;"
                )

    def _ingresar(self, usuario, clave, mensaje):
        try:
            datos = login_usuario(usuario, clave)
        except Exception:
            datos = None
        if not datos:
            mensaje.set_content(
                '<div style="background:rgba(230,57,70,.14);border:1px solid #e63946;'
                'border-radius:14px;padding:12px;color:#ff9aa3;font-size:13px;'
                'margin-bottom:14px;">Credenciales incorrectas.</div>'
            )
            return
        guardar_sesion(datos)
        ui.notify("Acceso correcto", color="positive")
        ui.navigate.to("/admin")

    @staticmethod
    def _fondo():
        ui.html('''<div style="position:fixed;inset:0;background:
          radial-gradient(circle at 20% 40%,rgba(230,57,70,.18),transparent 28%),
          radial-gradient(circle at 80% 45%,rgba(230,57,70,.12),transparent 28%),
          linear-gradient(135deg,#070707,#120707 52%,#050505);z-index:-2;"></div>''')

    @staticmethod
    def _encabezado():
        ui.html('''<div style="text-align:center;margin-bottom:24px;">
          <div style="font-size:25px;font-weight:900;color:#fff;margin-bottom:8px;">Auto<span style="color:#e63946;">Ventas</span> Pro</div>
          <div style="font-size:28px;font-weight:900;color:#fff;">Ingreso del equipo comercial</div>
          <p style="color:#999;font-size:14px;line-height:1.6;margin:8px 0 0;">Gerente y asesores usan el mismo acceso; cada rol ve únicamente lo que le corresponde.</p>
          <p style="color:#777;font-size:12px;margin-top:12px;">Credenciales académicas disponibles en README.md.</p>
        </div>''')


def login():
    LoginPage().render()
