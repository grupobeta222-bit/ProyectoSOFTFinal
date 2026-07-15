import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.application.services.cotizacion_service import CotizacionService
from src.domain.exceptions.domain_exception import DomainException
from src.infrastructure.db_connection import asegurar_migraciones_basicas
from src.infrastructure.repositories.sqlite_cotizacion_repository import SqliteCotizacionRepository
from src.infrastructure.repositories.sqlite_plan_repository import SqlitePlanRepository
from src.infrastructure.repositories.sqlite_vehiculo_repository import SqliteVehiculoRepository
from src.interfaces.controllers.cotizacion_controller import CotizacionController


def crear_servicio():
    vehiculo_repo = SqliteVehiculoRepository()
    plan_repo = SqlitePlanRepository()
    cotizacion_repo = SqliteCotizacionRepository()
    return CotizacionService(vehiculo_repo, plan_repo, cotizacion_repo)


def mostrar_tabla(servicio, cotizacion_id):
    resultado = servicio.obtener_tabla_amortizacion(cotizacion_id)
    tabla = resultado["tabla_amortizacion"]

    print("\n[DEMO] Tabla de amortizacion (primeras 5 cuotas)...")
    print("\n  {:>5}  {:>14}  {:>12}  {:>12}  {:>12}  {:>12}".format(
        "#", "Saldo Inicial", "Capital", "Interes", "Cuota Total", "Saldo Final"
    ))
    print("  " + "-" * 74)

    for fila in tabla[:5]:
        print("  {:>5}  ${:>13,.2f}  ${:>11,.2f}  ${:>11,.2f}  ${:>11,.2f}  ${:>11,.2f}".format(
            fila["cuota"],
            fila["saldo_inicial"],
            fila["capital"],
            fila["interes"],
            fila["cuota_total"],
            fila["saldo_final"],
        ))
    print("  ... (tabla completa con ver_tabla_amortizacion)")


def demo_cotizacion(controller, servicio):
    print("\n[DEMO] Generando cotizacion de ejemplo...")
    cotizacion = controller.generar_cotizacion(
        vehiculo_id="VEH001",
        plan_id="PLAN001",
        nombre_cliente="Maria Fernanda Torres",
        email_cliente="mfernanda@gmail.com",
        cedula_cliente="0912345678",
        telefono_cliente="0991234567",
        entrada=6000.0,
        plazo_meses=24,
    )
    mostrar_tabla(servicio, cotizacion.id)


def demo_entrada_insuficiente(controller):
    print("\n[DEMO] Validacion: entrada insuficiente (debe fallar)...")
    try:
        controller.generar_cotizacion(
            vehiculo_id="VEH001",
            plan_id="PLAN001",
            nombre_cliente="Pedro Alvarado",
            email_cliente="pedro@mail.com",
            cedula_cliente="0987654321",
            telefono_cliente="0991111111",
            entrada=100.0,
            plazo_meses=24,
        )
    except DomainException:
        print("  OK - Validacion de entrada minima funcionando correctamente.")


def demo_plazo_no_valido(controller):
    print("\n[DEMO] Validacion: plazo no disponible (debe fallar)...")
    try:
        controller.generar_cotizacion(
            vehiculo_id="VEH001",
            plan_id="PLAN001",
            nombre_cliente="Ana Lopez",
            email_cliente="ana@mail.com",
            cedula_cliente="0912312312",
            telefono_cliente="0992222222",
            entrada=6000.0,
            plazo_meses=72,
        )
    except DomainException:
        print("  OK - Validacion de plazo funcionando correctamente.")


def main():
    print("\n" + "=" * 70)
    print("  AUTOVENTAS PRO")
    print("  Arquitectura Hexagonal | SQLite local | Repository Pattern")
    print("=" * 70)

    asegurar_migraciones_basicas()
    servicio = crear_servicio()
    controller = CotizacionController(servicio)

    controller.listar_vehiculos()
    controller.listar_planes()

    try:
        demo_cotizacion(controller, servicio)
    except DomainException as error:
        print("\n[ERROR] " + str(error))
    except Exception as error:
        print("\n[ERROR BD] La base local no esta disponible o hubo un error.")
        print("Detalle: " + str(error))
        print("Asegurese de tener permisos de escritura en la carpeta.")

    demo_entrada_insuficiente(controller)
    demo_plazo_no_valido(controller)
    controller.listar_cotizaciones()

    print("\nDemostracion completada. Datos guardados en SQLite local.")
    print("Base de datos: autoventas.db\n")


if __name__ == "__main__":
    main()
