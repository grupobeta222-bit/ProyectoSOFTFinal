import pathlib
import sys

from nicegui import app, ui

ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.application.container import AppContainer
from src.domain.entities.cliente import Cliente
from src.domain.entities.cotizacion import Cotizacion
from src.domain.entities.plan_financiamiento import PlanFinanciamiento
from src.domain.entities.vehiculo import Vehiculo
from src.domain.exceptions.domain_exception import DomainException
from src.interfaces.presentation.helpers import (
    car_image_src,
    car_media,
    emoji_auto,
    estado_normalizado,
    estado_texto,
    money,
)

ASSETS_DIR = pathlib.Path(__file__).resolve().parent / "assets"
if ASSETS_DIR.exists():
    app.add_static_files("/assets", str(ASSETS_DIR))

DB = False
DB_ERR = ""
container = None
svc = None

try:
    container = AppContainer()
    svc = container.cotizacion_service
    DB = True
except Exception as error:
    DB_ERR = str(error)


def _servicio_disponible():
    if not DB or container is None:
        raise DomainException("No se pudo conectar con la base local: " + DB_ERR)


ASESORES = container.auth_service.listar_asesores() if DB else []


def login_usuario(usuario, clave):
    _servicio_disponible()
    return container.auth_service.autenticar(usuario, clave)


def guardar_sesion(datos):
    app.storage.user["admin_logged"] = True
    app.storage.user["rol"] = datos.get("rol")
    app.storage.user["nombre"] = datos.get("nombre")
    app.storage.user["asesor_id"] = datos.get("asesor_id")


def cerrar_sesion_admin():
    for clave in ["admin_logged", "rol", "nombre", "asesor_id"]:
        app.storage.user.pop(clave, None)


def admin_logueado():
    return bool(app.storage.user.get("admin_logged", False))


def usuario_actual():
    if not admin_logueado():
        return {"rol": "publico", "nombre": "Visitante", "asesor_id": None}
    return {
        "rol": app.storage.user.get("rol", "gerente"),
        "nombre": app.storage.user.get("nombre", "Usuario"),
        "asesor_id": app.storage.user.get("asesor_id"),
    }


def es_gerente():
    return usuario_actual()["rol"] == "gerente"


def asesor_actual_id():
    return usuario_actual().get("asesor_id")


def buscar_asesor(asesor_id):
    for asesor in ASESORES:
        if asesor["id"] == asesor_id:
            return asesor
    return None


def get_vehiculos():
    _servicio_disponible()
    return svc.listar_vehiculos()


def get_planes():
    _servicio_disponible()
    return svc.listar_planes()


def buscar_por_id(datos, codigo):
    for item in datos:
        if item.id == codigo:
            return item
    return None


def _cotizaciones_visibles(cotizaciones):
    usuario = usuario_actual()
    if usuario["rol"] in ["gerente", "publico"]:
        return cotizaciones
    return [
        cotizacion for cotizacion in cotizaciones
        if cotizacion.asesor_id == usuario["asesor_id"]
    ]


def _siguiente_asesor_id():
    if asesor_actual_id():
        return asesor_actual_id()
    total = len(svc.listar_cotizaciones())
    return (total % len(ASESORES)) + 1


def generar_cotizacion_segura(vehiculo_id, plan_id, nombre_cliente, email_cliente,
                              entrada, plazo_meses, cedula_cliente="", telefono_cliente="",
                              ciudad_cliente=""):
    _servicio_disponible()
    cotizacion = svc.generar_cotizacion(
        vehiculo_id=vehiculo_id,
        plan_id=plan_id,
        nombre_cliente=nombre_cliente,
        email_cliente=email_cliente,
        cedula_cliente=cedula_cliente,
        telefono_cliente=telefono_cliente,
        ciudad_cliente=ciudad_cliente,
        asesor_id=_siguiente_asesor_id(),
        entrada=float(entrada),
        plazo_meses=int(plazo_meses),
    )
    resultado = svc.obtener_tabla_amortizacion(cotizacion.id)
    return cotizacion, resultado["tabla_amortizacion"], True


def get_cotizaciones():
    _servicio_disponible()
    return _cotizaciones_visibles(svc.listar_cotizaciones())


def get_clientes():
    _servicio_disponible()
    clientes = svc.listar_clientes()
    if es_gerente():
        return clientes
    claves = {item.cedula_cliente or item.email_cliente for item in get_cotizaciones()}
    return [item for item in clientes if (item.cedula or item.email) in claves]


def cambiar_estado_cotizacion_segura(cotizacion_id, nuevo_estado):
    usuario = usuario_actual()
    return svc.cambiar_estado_cotizacion(
        cotizacion_id,
        nuevo_estado,
        rol=usuario["rol"],
        usuario_asesor_id=usuario["asesor_id"],
    )


def get_testimonios():
    _servicio_disponible()
    return container.testimonio_service.listar()


def publicar_testimonio(nombre, email, texto, foto_url="", calificacion=5):
    _servicio_disponible()
    return container.testimonio_service.publicar(
        nombre, email, texto, foto_url, calificacion
    )


def registrar_cliente(nombre, email, cedula, telefono, password):
    _servicio_disponible()
    return container.cliente_service.registrar(
        nombre, email, cedula, telefono, password
    )


def login_cliente(email, password):
    _servicio_disponible()
    return container.cliente_service.autenticar(email, password)


def guardar_sesion_cliente(datos):
    app.storage.user["cliente_logged"] = True
    app.storage.user["cliente_data"] = datos


def cerrar_sesion_cliente():
    app.storage.user.pop("cliente_logged", None)
    app.storage.user.pop("cliente_data", None)


def cliente_logueado():
    return bool(app.storage.user.get("cliente_logged", False))


def get_cliente_actual():
    return app.storage.user.get("cliente_data", {})


def get_cotizaciones_cliente(email):
    _servicio_disponible()
    return container.cliente_service.cotizaciones_por_email(email)


def actualizar_cliente_perfil(email, nombre, telefono, cedula, password):
    _servicio_disponible()
    return container.cliente_service.actualizar_perfil(
        email, nombre, telefono, cedula, password
    )


def get_notificaciones():
    usuario = usuario_actual()
    return container.notificacion_service.listar(
        get_cotizaciones(), usuario["rol"], usuario["asesor_id"]
    )


def add_css():
    ui.add_head_html('<link rel="stylesheet" href="/assets/styles.css?v=21">')
