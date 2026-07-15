from src.interfaces.presentation.context import ui


def _input_cliente(label, value=None):
    campo = ui.input(label=label, value=value)
    campo.props("outlined stack-label")
    return campo


def crear_campos_cliente():
    """Campos del cliente usados en el cotizador.

    Código simple: solo crea los campos y los devuelve para que la página
    de cotización pueda leer sus valores.
    """
    with ui.element("div").classes("av-form-space"):
        nombre = _input_cliente("Nombre completo")
        email = _input_cliente("Correo electrónico")
        cedula = _input_cliente("Cédula (10 dígitos)")
        telefono = _input_cliente("Teléfono")
        ciudad = _input_cliente("Ciudad")
    return nombre, email, cedula, telefono, ciudad

