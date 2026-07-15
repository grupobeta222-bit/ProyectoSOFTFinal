from src.domain.exceptions.domain_exception import DomainException


class PlanFinanciamiento:

    def __init__(self, id, nombre, entrada_minima_porcentaje,
                 tasa_anual, plazos_disponibles, comision_apertura=0.0, activo=True):
        self.id                        = id
        self.nombre                    = nombre
        self.entrada_minima_porcentaje = entrada_minima_porcentaje
        self.tasa_anual                = tasa_anual
        self.plazos_disponibles        = plazos_disponibles
        self.comision_apertura         = comision_apertura
        self.activo                    = bool(activo)
        self._validar()

    def _validar(self):
        if not self.id or not self.id.strip():
            raise DomainException("El ID del plan no puede estar vacío.")

        if not self.nombre or not self.nombre.strip():
            raise DomainException("El nombre del plan no puede estar vacío.")

        if self.entrada_minima_porcentaje <= 0 or self.entrada_minima_porcentaje >= 100:
            raise DomainException("El porcentaje de entrada debe estar entre 1 y 99.")

        if self.tasa_anual <= 0:
            raise DomainException("La tasa anual debe ser mayor a cero.")

        if not self.plazos_disponibles:
            raise DomainException("El plan debe tener al menos un plazo disponible.")

        if any(plazo <= 0 for plazo in self.plazos_disponibles):
            raise DomainException("Los plazos del plan deben ser mayores a cero.")

        if self.comision_apertura < 0:
            raise DomainException("La comisión no puede ser negativa.")

    def plazo_es_valido(self, plazo_meses):
        return self.activo and plazo_meses in self.plazos_disponibles

    def calcular_entrada_minima(self, precio_vehiculo):
        return precio_vehiculo * (self.entrada_minima_porcentaje / 100)

    def __str__(self):
        plazos = ", ".join(str(p) for p in self.plazos_disponibles)
        return self.nombre + " | Tasa: " + str(self.tasa_anual) + "% | Plazos: " + plazos + " meses"
