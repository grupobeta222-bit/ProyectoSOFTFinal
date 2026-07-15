import pathlib
import sys
import os

ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.interfaces.presentation.context import app, ui
from src.interfaces.presentation.pages.admin_clientes_page import admin_clientes
from src.interfaces.presentation.pages.admin_cotizaciones_page import admin_cotizaciones
from src.interfaces.presentation.pages.admin_dashboard_page import admin_dashboard
from src.interfaces.presentation.pages.admin_planes_page import admin_planes
from src.interfaces.presentation.pages.admin_vehiculos_page import admin_vehiculos
from src.interfaces.presentation.pages.asistente_page import asistente
from src.interfaces.presentation.pages.catalogo_page import catalogo
from src.interfaces.presentation.pages.cliente_dashboard_page import cliente_dashboard
from src.interfaces.presentation.pages.cliente_login_page import cliente_login
from src.interfaces.presentation.pages.contacto_page import contacto
from src.interfaces.presentation.pages.cotizacion_page import cotizar
from src.interfaces.presentation.pages.financiamiento_page import financiamiento
from src.interfaces.presentation.pages.home_page import landing
from src.interfaces.presentation.pages.login_page import login
from src.interfaces.presentation.pages.vehiculo_detalle_page import vehiculo_detalle


@ui.page("/")
def pagina_inicio():
    landing()


@ui.page("/catalogo")
def pagina_catalogo():
    catalogo()


@ui.page("/vehiculos")
def pagina_vehiculos():
    catalogo()


@ui.page("/vehiculo/{vehiculo_id}")
def pagina_detalle(vehiculo_id: str):
    vehiculo_detalle(vehiculo_id.replace("-", ""))


@ui.page("/financiamiento")
def pagina_financiamiento():
    financiamiento()


@ui.page("/cotizar")
def pagina_cotizar():
    cotizar()


@ui.page("/asistente")
def pagina_asistente():
    asistente()


@ui.page("/contacto")
def pagina_contacto():
    contacto()


@ui.page("/login")
def pagina_login():
    login()


@ui.page("/admin")
def pagina_admin():
    admin_dashboard()


@ui.page("/admin/cotizaciones")
def pagina_admin_cotizaciones():
    admin_cotizaciones()


@ui.page("/admin/vehiculos")
def pagina_admin_vehiculos():
    admin_vehiculos()


@ui.page("/admin/planes")
def pagina_admin_planes():
    admin_planes()


@ui.page("/admin/clientes")
def pagina_admin_clientes():
    admin_clientes()


@ui.page("/ingreso")
def pagina_ingreso_cliente():
    cliente_login()


@ui.page("/mi-panel")
def pagina_panel_cliente():
    cliente_dashboard()


if __name__ in ["__main__", "__mp_main__"]:
    ui.run(
        title="AutoVentas Pro",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        show=False,
        reload=False,
        favicon="🚗",
        storage_secret="autoventas-pro-admin",
    )