import pytest

from src.domain.entities.vehiculo          import Vehiculo
from src.domain.entities.plan_financiamiento import PlanFinanciamiento
from src.domain.entities.cotizacion        import Cotizacion
from src.domain.entities.cliente           import Cliente
from src.domain.exceptions.domain_exception import DomainException


class TestVehiculo:

    def test_vehiculo_valido(self):
        v = Vehiculo(id="VEH001", marca="Toyota", modelo="Corolla",
                     anio=2025, precio_base=25990.0, stock=5)
        assert v.tiene_stock() == True

    def test_vehiculo_sin_stock(self):
        v = Vehiculo(id="VEH001", marca="Toyota", modelo="Corolla",
                     anio=2025, precio_base=25990.0, stock=0)
        assert v.tiene_stock() == False

    def test_precio_negativo_lanza_error(self):
        with pytest.raises(DomainException):
            Vehiculo(id="VEH001", marca="Toyota", modelo="Corolla",
                     anio=2025, precio_base=-100.0, stock=1)

    def test_anio_antiguo_lanza_error(self):
        with pytest.raises(DomainException):
            Vehiculo(id="VEH001", marca="Toyota", modelo="Corolla",
                     anio=1990, precio_base=10000.0, stock=1)

    def test_id_vacio_lanza_error(self):
        with pytest.raises(DomainException):
            Vehiculo(id="", marca="Toyota", modelo="Corolla",
                     anio=2025, precio_base=10000.0, stock=1)


class TestPlanFinanciamiento:

    def test_plan_valido(self):
        p = PlanFinanciamiento(
            id="PLAN001", nombre="Clasico",
            entrada_minima_porcentaje=20, tasa_anual=12.5,
            plazos_disponibles=[12, 24, 36],
        )
        assert p.plazo_es_valido(24) == True
        assert p.plazo_es_valido(72) == False

    def test_calculo_entrada_minima(self):
        p = PlanFinanciamiento(
            id="PLAN001", nombre="Clasico",
            entrada_minima_porcentaje=20, tasa_anual=12.5,
            plazos_disponibles=[12, 24, 36],
        )
        resultado = p.calcular_entrada_minima(25990.0)
        assert abs(resultado - 5198.0) < 0.01

    def test_sin_plazos_lanza_error(self):
        with pytest.raises(DomainException):
            PlanFinanciamiento(
                id="PLAN001", nombre="Clasico",
                entrada_minima_porcentaje=20, tasa_anual=12.5,
                plazos_disponibles=[],
            )

    def test_tasa_cero_lanza_error(self):
        with pytest.raises(DomainException):
            PlanFinanciamiento(
                id="PLAN001", nombre="Clasico",
                entrada_minima_porcentaje=20, tasa_anual=0,
                plazos_disponibles=[12],
            )


class TestCotizacion:

    def crear_cotizacion(self, **cambios):
        datos = dict(
            id              = "COT-TEST01",
            vehiculo_id     = "VEH001",
            plan_id         = "PLAN001",
            nombre_cliente  = "Test User",
            email_cliente   = "test@mail.com",
            precio_vehiculo = 25990.0,
            entrada         = 6000.0,
            plazo_meses     = 24,
            tasa_anual      = 12.5,
        )
        datos.update(cambios)
        return Cotizacion(**datos)

    def test_cuota_mayor_a_cero(self):
        cot = self.crear_cotizacion()
        assert cot.cuota_mensual > 0

    def test_monto_financiado_correcto(self):
        cot = self.crear_cotizacion()
        assert cot.monto_financiado == 25990.0 - 6000.0

    def test_tabla_tiene_24_filas(self):
        cot   = self.crear_cotizacion()
        tabla = cot.generar_tabla_amortizacion()
        assert len(tabla) == 24

    def test_ultimo_saldo_es_cero(self):
        cot   = self.crear_cotizacion()
        tabla = cot.generar_tabla_amortizacion()
        assert tabla[-1]["saldo_final"] == 0.0

    def test_entrada_mayor_precio_lanza_error(self):
        with pytest.raises(DomainException):
            self.crear_cotizacion(entrada=30000.0)

    def test_estado_invalido_lanza_error(self):
        with pytest.raises(DomainException):
            self.crear_cotizacion(estado="inventado")

    def test_to_dict_tiene_datos_cliente(self):
        cot = self.crear_cotizacion()
        d   = cot.to_dict()
        assert d["id"]                  == "COT-TEST01"
        assert d["cliente"]["email"]    == "test@mail.com"
        assert d["monto_financiado"]    == 19990.0


class TestCliente:

    def test_cliente_valido(self):
        c = Cliente(nombre="Juan Perez", email="juan@mail.com",
                    cedula="0912345678", telefono="0991234567")
        assert c.nombre == "Juan Perez"

    def test_nombre_corto_lanza_error(self):
        with pytest.raises(DomainException):
            Cliente(nombre="AB", email="ab@mail.com")

    def test_email_sin_arroba_lanza_error(self):
        with pytest.raises(DomainException):
            Cliente(nombre="Juan Perez", email="sinArroba.com")

    def test_cedula_con_letras_lanza_error(self):
        with pytest.raises(DomainException):
            Cliente(nombre="Juan Perez", email="j@mail.com", cedula="091234ABCD")

    def test_cedula_menos_de_10_digitos_lanza_error(self):
        with pytest.raises(DomainException):
            Cliente(nombre="Juan Perez", email="j@mail.com", cedula="12345")
