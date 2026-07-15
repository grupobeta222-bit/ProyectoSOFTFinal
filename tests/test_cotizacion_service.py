import pytest
from unittest.mock import MagicMock

from src.application.services.cotizacion_service import CotizacionService
from src.domain.entities.vehiculo import Vehiculo
from src.domain.entities.plan_financiamiento import PlanFinanciamiento
from src.domain.exceptions.domain_exception import DomainException


def crear_vehiculo_prueba():
    return Vehiculo(
        id          = "VEH001",
        marca       = "Toyota",
        modelo      = "Corolla",
        anio        = 2025,
        precio_base = 25990.0,
        stock       = 5,
        motor       = "1.8L",
        transmision = "Automatica",
        combustible = "Gasolina",
    )


def crear_plan_prueba():
    return PlanFinanciamiento(
        id                        = "PLAN001",
        nombre                    = "Plan Clasico",
        entrada_minima_porcentaje = 20,
        tasa_anual                = 12.5,
        plazos_disponibles        = [12, 24, 36],
        comision_apertura         = 200.0,
    )


def crear_servicio(vehiculo=None, plan=None):
    vehiculo_repo   = MagicMock()
    plan_repo       = MagicMock()
    cotizacion_repo = MagicMock()

    vehiculo_repo.find_by_id.return_value   = vehiculo or crear_vehiculo_prueba()
    plan_repo.find_by_id.return_value       = plan or crear_plan_prueba()
    cliente_repo = MagicMock()
    cotizacion_repo.find_all.return_value      = []
    cotizacion_repo.find_by_id.return_value    = None
    cotizacion_repo.save.return_value          = None
    cotizacion_repo.update_estado.return_value = True

    return CotizacionService(vehiculo_repo, plan_repo, cotizacion_repo, cliente_repo)


class TestGenerarCotizacion:

    def test_cotizacion_valida(self):
        servicio   = crear_servicio()
        cotizacion = servicio.generar_cotizacion(
            vehiculo_id      = "VEH001",
            plan_id          = "PLAN001",
            nombre_cliente   = "Maria Perez",
            email_cliente    = "maria@mail.com",
            cedula_cliente   = "0912345678",
            telefono_cliente = "0991234567",
            entrada          = 6000.0,
            plazo_meses      = 24,
        )
        assert cotizacion.id.startswith("COT-")
        assert cotizacion.estado          == "pendiente"
        assert cotizacion.monto_financiado == 25990.0 - 6000.0
        assert cotizacion.cuota_mensual   > 0

    def test_vehiculo_no_existe(self):
        servicio = crear_servicio()
        servicio.vehiculo_repo.find_by_id.return_value = None

        with pytest.raises(DomainException):
            servicio.generar_cotizacion(
                vehiculo_id    = "VEH999",
                plan_id        = "PLAN001",
                nombre_cliente = "X",
                email_cliente  = "x@x.com",
                entrada        = 5000.0,
                plazo_meses    = 24,
            )

    def test_vehiculo_sin_stock(self):
        vehiculo       = crear_vehiculo_prueba()
        vehiculo.stock = 0
        servicio       = crear_servicio(vehiculo=vehiculo)

        with pytest.raises(DomainException):
            servicio.generar_cotizacion(
                vehiculo_id    = "VEH001",
                plan_id        = "PLAN001",
                nombre_cliente = "X",
                email_cliente  = "x@x.com",
                entrada        = 5000.0,
                plazo_meses    = 24,
            )

    def test_plan_no_existe(self):
        servicio = crear_servicio()
        servicio.plan_repo.find_by_id.return_value = None

        with pytest.raises(DomainException):
            servicio.generar_cotizacion(
                vehiculo_id    = "VEH001",
                plan_id        = "PLAN999",
                nombre_cliente = "X",
                email_cliente  = "x@x.com",
                entrada        = 5000.0,
                plazo_meses    = 24,
            )

    def test_entrada_insuficiente(self):
        servicio = crear_servicio()

        with pytest.raises(DomainException):
            servicio.generar_cotizacion(
                vehiculo_id    = "VEH001",
                plan_id        = "PLAN001",
                nombre_cliente = "X",
                email_cliente  = "x@x.com",
                entrada        = 100.0,
                plazo_meses    = 24,
            )

    def test_plazo_no_valido(self):
        servicio = crear_servicio()

        with pytest.raises(DomainException):
            servicio.generar_cotizacion(
                vehiculo_id    = "VEH001",
                plan_id        = "PLAN001",
                nombre_cliente = "X",
                email_cliente  = "x@x.com",
                entrada        = 6000.0,
                plazo_meses    = 72,
            )


class TestTablaAmortizacion:

    def test_tabla_tiene_numero_correcto_de_filas(self):
        servicio   = crear_servicio()
        cotizacion = servicio.generar_cotizacion(
            vehiculo_id      = "VEH001",
            plan_id          = "PLAN001",
            nombre_cliente   = "Ana Lopez",
            email_cliente    = "ana@mail.com",
            cedula_cliente   = "0987654321",
            telefono_cliente = "0991111111",
            entrada          = 6000.0,
            plazo_meses      = 24,
        )
        servicio.cotizacion_repo.find_by_id.return_value = cotizacion

        resultado = servicio.obtener_tabla_amortizacion(cotizacion.id)
        tabla     = resultado["tabla_amortizacion"]

        assert len(tabla) == 24
        assert tabla[-1]["saldo_final"] == 0.0

    def test_cotizacion_inexistente_lanza_error(self):
        servicio = crear_servicio()
        servicio.cotizacion_repo.find_by_id.return_value = None

        with pytest.raises(DomainException):
            servicio.obtener_tabla_amortizacion("COT-INEXISTENTE")



class TestCambioEstadoCotizacion:

    def test_cambiar_estado_en_revision(self):
        servicio = crear_servicio()
        cotizacion = servicio.generar_cotizacion(
            vehiculo_id      = "VEH001",
            plan_id          = "PLAN001",
            nombre_cliente   = "Carlos Perez",
            email_cliente    = "carlos@mail.com",
            cedula_cliente   = "0911111111",
            telefono_cliente = "0991111111",
            entrada          = 6000.0,
            plazo_meses      = 24,
        )
        servicio.cotizacion_repo.find_by_id.return_value = cotizacion

        actualizada = servicio.cambiar_estado_cotizacion(cotizacion.id, "en_revision")

        assert actualizada.estado == "en_revision"
        servicio.cotizacion_repo.update_estado.assert_called_once_with(cotizacion.id, "en_revision")

    def test_cambiar_estado_invalido(self):
        servicio = crear_servicio()
        with pytest.raises(DomainException):
            servicio.cambiar_estado_cotizacion("COT-TEST", "inventado")
