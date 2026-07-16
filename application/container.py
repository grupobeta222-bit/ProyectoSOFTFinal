from src.application.services.auth_service import AuthService
from src.application.services.cliente_service import ClienteService
from src.application.services.contacto_service import ContactoService
from src.application.services.cotizacion_service import CotizacionService
from src.application.services.dashboard_service import DashboardService
from src.application.services.notificacion_service import NotificacionService
from src.application.services.testimonio_service import TestimonioService
from src.infrastructure.db_connection import DatabaseManager
from src.infrastructure.repositories.sqlite_cliente_repository import SqliteClienteRepository
from src.infrastructure.repositories.sqlite_cotizacion_repository import SqliteCotizacionRepository
from src.infrastructure.repositories.sqlite_plan_repository import SqlitePlanRepository
from src.infrastructure.repositories.sqlite_testimonio_repository import SqliteTestimonioRepository
from src.infrastructure.repositories.sqlite_usuario_repository import SqliteUsuarioRepository
from src.infrastructure.repositories.sqlite_vehiculo_repository import SqliteVehiculoRepository


class AppContainer:
    def __init__(self):
        DatabaseManager().inicializar()
        self.vehiculos = SqliteVehiculoRepository()
        self.planes = SqlitePlanRepository()
        self.cotizaciones = SqliteCotizacionRepository()
        self.clientes = SqliteClienteRepository()
        self.usuarios = SqliteUsuarioRepository()
        self.testimonios = SqliteTestimonioRepository()

        self.cotizacion_service = CotizacionService(
            self.vehiculos, self.planes, self.cotizaciones, self.clientes
        )
        self.auth_service = AuthService(self.usuarios)
        self.cliente_service = ClienteService(self.clientes, self.cotizaciones)
        self.testimonio_service = TestimonioService(self.testimonios, self.clientes)
        self.dashboard_service = DashboardService(self.cotizaciones, self.usuarios)
        self.notificacion_service = NotificacionService()
        self.contacto_service = ContactoService()
