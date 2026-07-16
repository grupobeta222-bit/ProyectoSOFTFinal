from src.application.factories.cotizacion_factory import CotizacionFactory
from src.domain.entities.cliente import Cliente
from src.domain.entities.cotizacion import EstadoCotizacion
from src.domain.entities.plan_financiamiento import PlanFinanciamiento
from src.domain.entities.vehiculo import Vehiculo
from src.domain.exceptions.domain_exception import DomainException


class CotizacionService:
    ESTADOS_COTIZACION = ["pendiente", "en_revision", "aprobada", "rechazada", "cerrada"]

    def __init__(self, vehiculo_repo, plan_repo, cotizacion_repo, cliente_repo=None,
                 factory=None):
        self.vehiculo_repo = vehiculo_repo
        self.plan_repo = plan_repo
        self.cotizacion_repo = cotizacion_repo
        self.cliente_repo = cliente_repo
        self.factory = factory or CotizacionFactory()

    def generar_cotizacion(self, vehiculo_id, plan_id, nombre_cliente, email_cliente,
                           entrada, plazo_meses, cedula_cliente="", telefono_cliente="",
                           ciudad_cliente="", asesor_id=1):
        vehiculo = self.vehiculo_repo.find_by_id(vehiculo_id)
        if vehiculo is None:
            raise DomainException("No se encontró el vehículo con ID: " + vehiculo_id)
        if not vehiculo.tiene_stock():
            raise DomainException("El vehículo " + vehiculo_id + " no tiene stock disponible.")

        plan = self.plan_repo.find_by_id(plan_id)
        if plan is None:
            raise DomainException("No se encontró el plan con ID: " + plan_id)

        cliente = Cliente(
            nombre=nombre_cliente,
            email=email_cliente,
            cedula=cedula_cliente,
            telefono=telefono_cliente,
            ciudad=ciudad_cliente,
        )

        entrada_minima = plan.calcular_entrada_minima(vehiculo.precio_base)
        if entrada < entrada_minima:
            mensaje = "La entrada mínima para el " + plan.nombre
            mensaje = mensaje + " es $" + str(round(entrada_minima, 2))
            mensaje = mensaje + ". Se ingresó: $" + str(entrada)
            raise DomainException(mensaje)

        if not plan.plazo_es_valido(plazo_meses):
            mensaje = "El plazo de " + str(plazo_meses) + " meses no está en el plan " + plan.nombre
            mensaje = mensaje + ". Plazos disponibles: " + str(plan.plazos_disponibles)
            raise DomainException(mensaje)

        cotizacion = self.factory.crear(
            vehiculo, plan, cliente, entrada, plazo_meses, asesor_id
        )

        self.cotizacion_repo.save(cotizacion)
        return cotizacion

    def listar_vehiculos(self):
        return self.vehiculo_repo.find_all()

    def listar_planes(self):
        return self.plan_repo.find_all()

    def listar_clientes(self):
        if self.cliente_repo is None:
            return []
        return self.cliente_repo.find_all()

    def listar_cotizaciones(self):
        return self.cotizacion_repo.find_all()

    def buscar_cotizacion(self, cotizacion_id):
        cotizacion = self.cotizacion_repo.find_by_id(cotizacion_id)
        if cotizacion is None:
            raise DomainException("No se encontró la cotización con ID: " + cotizacion_id)
        return cotizacion

    def buscar_cotizaciones_cliente(self, cedula):
        return self.cotizacion_repo.find_by_cedula(cedula)

    def cambiar_estado_cotizacion(self, cotizacion_id, nuevo_estado,
                                  rol="gerente", usuario_asesor_id=None):
        if nuevo_estado not in self.ESTADOS_COTIZACION:
            raise DomainException("Estado inválido: " + str(nuevo_estado))

        cotizacion = self.buscar_cotizacion(cotizacion_id)
        self._validar_permiso(cotizacion, nuevo_estado, rol, usuario_asesor_id)
        cotizacion.transicionar(nuevo_estado)

        if hasattr(self.cotizacion_repo, "update_estado"):
            if cotizacion.fecha_cierre:
                actualizado = self.cotizacion_repo.update_estado(
                    cotizacion_id, nuevo_estado, cotizacion.fecha_cierre
                )
            else:
                actualizado = self.cotizacion_repo.update_estado(
                    cotizacion_id, nuevo_estado
                )
        else:
            self.cotizacion_repo.save(cotizacion)
            actualizado = True

        if not actualizado:
            raise DomainException("No se pudo actualizar el estado de la cotización.")
        return cotizacion

    def _validar_permiso(self, cotizacion, nuevo_estado, rol, usuario_asesor_id):
        if rol == "asesor":
            if usuario_asesor_id != cotizacion.asesor_id:
                raise DomainException("Solo el asesor asignado puede actualizar esta cotización.")
            permitidos = {
                (EstadoCotizacion.PENDIENTE.value, EstadoCotizacion.EN_REVISION.value),
                (EstadoCotizacion.APROBADA.value, EstadoCotizacion.CERRADA.value),
            }
            if (cotizacion.estado, nuevo_estado) not in permitidos:
                raise DomainException("El asesor no puede realizar ese cambio de estado.")
        elif rol != "gerente":
            raise DomainException("No tiene permisos para cambiar el estado.")

    def actualizar_vehiculo(self, vehiculo_id, marca, modelo, anio, precio_base, stock,
                            motor="N/D", transmision="N/D", combustible="Gasolina",
                            activo=True):
        existe = self.vehiculo_repo.find_by_id(vehiculo_id)
        if existe is None:
            raise DomainException("No se encontró el vehículo con ID: " + vehiculo_id)

        vehiculo = Vehiculo(
            id=vehiculo_id,
            marca=marca,
            modelo=modelo,
            anio=int(anio),
            precio_base=float(precio_base),
            stock=int(stock),
            motor=motor,
            transmision=transmision,
            combustible=combustible,
            activo=activo,
        )

        if hasattr(self.vehiculo_repo, "update"):
            self.vehiculo_repo.update(vehiculo)
        else:
            self.vehiculo_repo.save(vehiculo)
        return vehiculo

    def desactivar_vehiculo(self, vehiculo_id):
        vehiculo = self.vehiculo_repo.find_by_id(vehiculo_id)
        if vehiculo is None:
            raise DomainException("No se encontró el vehículo con ID: " + vehiculo_id)

        return self.actualizar_vehiculo(
            vehiculo.id,
            vehiculo.marca,
            vehiculo.modelo,
            vehiculo.anio,
            vehiculo.precio_base,
            0,
            vehiculo.motor,
            vehiculo.transmision,
            vehiculo.combustible,
            False,
        )

    def actualizar_plan(self, plan_id, nombre, entrada_minima_porcentaje, tasa_anual,
                        plazos_disponibles, comision_apertura=0.0, activo=True):
        existe = self.plan_repo.find_by_id(plan_id)
        if existe is None:
            raise DomainException("No se encontró el plan con ID: " + plan_id)

        plazos = []
        for plazo in plazos_disponibles:
            plazos.append(int(plazo))

        plan = PlanFinanciamiento(
            id=plan_id,
            nombre=nombre,
            entrada_minima_porcentaje=float(entrada_minima_porcentaje),
            tasa_anual=float(tasa_anual),
            plazos_disponibles=plazos,
            comision_apertura=float(comision_apertura),
            activo=activo,
        )

        if hasattr(self.plan_repo, "update"):
            self.plan_repo.update(plan)
        else:
            self.plan_repo.save(plan)
        return plan

    def eliminar_plan(self, plan_id):
        plan = self.plan_repo.find_by_id(plan_id)
        if plan is None:
            raise DomainException("No se encontró el plan con ID: " + plan_id)
        plan.activo = False
        self.plan_repo.update(plan)
        return True

    def obtener_tabla_amortizacion(self, cotizacion_id):
        cotizacion = self.buscar_cotizacion(cotizacion_id)
        tabla = cotizacion.generar_tabla_amortizacion()
        return {
            "cotizacion": cotizacion.to_dict(),
            "tabla_amortizacion": tabla,
        }
