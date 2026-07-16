import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///autoventas.db")
CONNECT_ARGS = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _activar_claves_foraneas(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class DatabaseSeeder:
    ADMIN_HASH = (
        "pbkdf2_sha256$260000$ec5a4edb60921f0f0fdb6c489d8e48b6$"
        "6999be658468c14755973e83e43bde2a81e7cec45e8e49175977e1cd20e56c76"
    )
    ASESOR_HASH = (
        "pbkdf2_sha256$260000$b9403a10a47b9522a12a9d3845151804$"
        "71b13cc20ad42a6fbed596e4fe95d55119fa6a1b26b69d94b73fc856f58e9499"
    )
    CLIENTE_HASH = (
        "pbkdf2_sha256$260000$97a9e66f60b7c46235b2dfc1fcc0e173$"
        "ed88bfe6c8e40cf83aa70b8f64213d5354eaae242cabf1a4be9febb29f932c23"
    )

    def __init__(self, session):
        self.session = session

    def ejecutar(self):
        clientes = self._crear_clientes()
        self._crear_usuarios()
        self._crear_vehiculos()
        self._crear_planes()
        self.session.flush()
        self._crear_cotizaciones(clientes)
        self._crear_testimonios(clientes)
        self.session.commit()

    def _crear_usuarios(self):
        from src.infrastructure.orm_models import UsuarioORM

        if self.session.query(UsuarioORM).count():
            return

        usuarios = [
            UsuarioORM(id=100, nombre="Gerente General", email="admin@autoventas.com",
                       password_hash=self.ADMIN_HASH, rol="gerente", rating=5),
            UsuarioORM(id=1, nombre="Josué Reyes Villón", email="asesor1@autoventas.com",
                       password_hash=self.ASESOR_HASH, rol="asesor",
                       especialidad="Dashboard y reportes", rating=4.8),
            UsuarioORM(id=2, nombre="José Reyes Pazos", email="asesor2@autoventas.com",
                       password_hash=self.ASESOR_HASH, rol="asesor",
                       especialidad="Cotización financiera", rating=4.7),
            UsuarioORM(id=3, nombre="Cristel Chancay Ávila", email="asesor3@autoventas.com",
                       password_hash=self.ASESOR_HASH, rol="asesor",
                       especialidad="Navegación y diseño", rating=4.8),
            UsuarioORM(id=4, nombre="Kristel Bonilla Navarro", email="asesor4@autoventas.com",
                       password_hash=self.ASESOR_HASH, rol="asesor",
                       especialidad="Clientes y acceso", rating=4.9),
            UsuarioORM(id=5, nombre="Nick Olives", email="asesor5@autoventas.com",
                       password_hash=self.ASESOR_HASH, rol="asesor",
                       especialidad="Catálogo y contacto", rating=4.7),
        ]
        self.session.add_all(usuarios)

    def _crear_clientes(self):
        from src.infrastructure.orm_models import ClienteORM

        existentes = self.session.query(ClienteORM).all()
        if existentes:
            return existentes

        clientes = [
            ClienteORM(nombre="Cliente Demo", email="cliente1@demo.com", cedula="0950123456",
                       telefono="0981112233", ciudad="Guayaquil",
                       password_hash=self.CLIENTE_HASH),
            ClienteORM(nombre="Carlos Mendoza", email="carlos.mendoza@demo.com",
                       cedula="0951123456", telefono="0982223344", ciudad="Quito"),
            ClienteORM(nombre="Andrea Vera", email="andrea.vera@demo.com",
                       cedula="0952123456", telefono="0983334455", ciudad="Cuenca"),
            ClienteORM(nombre="Luis Torres", email="luis.torres@demo.com",
                       cedula="0953123456", telefono="0984445566", ciudad="Manta"),
            ClienteORM(nombre="María Zambrano", email="maria.zambrano@demo.com",
                       cedula="0954123456", telefono="0985556677", ciudad="Loja"),
            ClienteORM(nombre="Daniel Paredes", email="daniel.paredes@demo.com",
                       cedula="0955123456", telefono="0986667788", ciudad="Ambato"),
        ]
        self.session.add_all(clientes)
        self.session.flush()
        return clientes

    def _crear_vehiculos(self):
        from src.infrastructure.orm_models import VehiculoORM

        if self.session.query(VehiculoORM).count():
            return

        datos = [
            ("VEH001", "Toyota", "Corolla", 25990, 5, "1.8L", "Automática", "Gasolina"),
            ("VEH002", "Toyota", "RAV4", 35990, 3, "2.5L", "Automática", "Híbrido"),
            ("VEH003", "Honda", "Civic", 27450, 4, "1.5L Turbo", "CVT", "Gasolina"),
            ("VEH004", "Honda", "CR-V", 38450, 2, "1.5L Turbo", "CVT", "Gasolina"),
            ("VEH005", "Ford", "Maverick", 32990, 6, "2.0L EcoBoost", "Automática", "Gasolina"),
            ("VEH006", "Chevrolet", "Tracker", 22990, 8, "1.2L Turbo", "Automática", "Gasolina"),
            ("VEH007", "Volkswagen", "Golf GTI", 33450, 3, "2.0L TSI", "Manual", "Gasolina"),
            ("VEH008", "Nissan", "Versa", 18990, 10, "1.6L", "CVT", "Gasolina"),
        ]
        for codigo, marca, modelo, precio, stock, motor, transmision, combustible in datos:
            self.session.add(VehiculoORM(
                id=codigo, marca=marca, modelo=modelo, anio=2025,
                precio_base=precio, stock=stock, motor=motor,
                transmision=transmision, combustible=combustible, activo=True,
            ))

    def _crear_planes(self):
        from src.infrastructure.orm_models import PlanFinanciamientoORM

        if self.session.query(PlanFinanciamientoORM).count():
            return

        self.session.add_all([
            PlanFinanciamientoORM(id="PLAN001", nombre="Plan Clásico",
                                  entrada_minima_porcentaje=20, tasa_anual=12.5,
                                  plazos_disponibles=[12, 24, 36], comision_apertura=200),
            PlanFinanciamientoORM(id="PLAN002", nombre="Plan Ejecutivo",
                                  entrada_minima_porcentaje=15, tasa_anual=10,
                                  plazos_disponibles=[12, 24, 36, 48, 60], comision_apertura=300),
            PlanFinanciamientoORM(id="PLAN003", nombre="Plan Premium",
                                  entrada_minima_porcentaje=10, tasa_anual=8.5,
                                  plazos_disponibles=[12, 24, 36, 48, 60, 72], comision_apertura=500),
        ])

    def _crear_cotizaciones(self, clientes):
        from src.domain.entities.cotizacion import Cotizacion
        from src.infrastructure.orm_models import CotizacionORM

        if self.session.query(CotizacionORM).count():
            return

        precios = [25990, 35990, 27450, 38450, 32990, 22990, 33450, 18990]
        planes = [
            ("PLAN001", 0.20, 12.5, 36, 200),
            ("PLAN002", 0.15, 10.0, 48, 300),
            ("PLAN003", 0.10, 8.5, 60, 500),
        ]
        estados = [
            "cerrada", "aprobada", "en_revision", "pendiente", "rechazada",
            "cerrada", "en_revision", "pendiente", "cerrada", "aprobada",
            "rechazada", "cerrada", "pendiente", "en_revision", "cerrada",
            "aprobada", "cerrada", "rechazada", "en_revision", "pendiente",
            "cerrada", "aprobada", "cerrada", "pendiente",
        ]
        hoy = datetime.now().replace(microsecond=0)

        for indice, estado in enumerate(estados, start=1):
            cliente = clientes[(indice - 1) % len(clientes)]
            vehiculo_pos = (indice - 1) % len(precios)
            plan_id, porcentaje, tasa, plazo, comision = planes[(indice - 1) % len(planes)]
            precio = precios[vehiculo_pos]
            entrada = round(precio * porcentaje, 2)
            fecha = hoy - timedelta(days=(indice - 1) * 4)
            entidad = Cotizacion(
                id="COT-DEMO-" + str(indice).zfill(3),
                vehiculo_id="VEH" + str(vehiculo_pos + 1).zfill(3),
                plan_id=plan_id,
                nombre_cliente=cliente.nombre,
                email_cliente=cliente.email,
                cedula_cliente=cliente.cedula or "",
                telefono_cliente=cliente.telefono or "",
                ciudad_cliente=cliente.ciudad or "",
                cliente_id=cliente.id,
                asesor_id=((indice - 1) % 5) + 1,
                precio_vehiculo=precio,
                entrada=entrada,
                plazo_meses=plazo,
                tasa_anual=tasa,
                comision_apertura=comision,
                estado=estado,
                fecha=fecha.strftime("%Y-%m-%dT%H:%M:%S"),
                fecha_cierre=(fecha + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S")
                if estado == "cerrada" else None,
            )
            self.session.add(CotizacionORM(
                id=entidad.id, cliente_id=cliente.id, vehiculo_id=entidad.vehiculo_id,
                plan_id=entidad.plan_id, asesor_id=entidad.asesor_id,
                precio_vehiculo=entidad.precio_vehiculo, entrada=entidad.entrada,
                plazo_meses=entidad.plazo_meses, tasa_anual=entidad.tasa_anual,
                comision_apertura=entidad.comision_apertura,
                cuota_mensual=entidad.cuota_mensual, estado=entidad.estado,
                fecha=fecha,
                fecha_cierre=fecha + timedelta(days=3) if estado == "cerrada" else None,
            ))

    def _crear_testimonios(self, clientes):
        from src.infrastructure.orm_models import TestimonioORM

        if self.session.query(TestimonioORM).count():
            return

        textos = [
            "La cotización fue rápida y pude revisar la cuota antes de decidir.",
            "La tabla de amortización me ayudó a entender bien el financiamiento.",
            "El asesor explicó el plan con claridad y el proceso fue sencillo.",
        ]
        for cliente, texto in zip(clientes[1:4], textos):
            self.session.add(TestimonioORM(
                cliente_id=cliente.id, texto=texto, calificacion=5, visible=True,
            ))


class DatabaseManager:
    def inicializar(self):
        import src.infrastructure.orm_models  # noqa: F401

        Base.metadata.create_all(bind=engine)
        with Session() as session:
            DatabaseSeeder(session).ejecutar()


def get_session():
    return Session()


def asegurar_migraciones_basicas():
    DatabaseManager().inicializar()
