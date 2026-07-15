from src.domain.exceptions.domain_exception import DomainException


class Vehiculo:

    def __init__(self, id, marca, modelo, anio, precio_base, stock,
                 motor="N/D", transmision="N/D", combustible="Gasolina", activo=True):
        self.id          = id
        self.marca       = marca
        self.modelo      = modelo
        self.anio        = anio
        self.precio_base = precio_base
        self.stock       = stock
        self.motor       = motor
        self.transmision = transmision
        self.combustible = combustible
        self.activo      = bool(activo)
        self._validar()

    def _validar(self):
        if not self.id or not self.id.strip():
            raise DomainException("El ID del vehículo no puede estar vacío.")

        if not self.marca or not self.marca.strip():
            raise DomainException("La marca no puede estar vacía.")

        if not self.modelo or not self.modelo.strip():
            raise DomainException("El modelo no puede estar vacío.")

        if self.anio < 2000:
            raise DomainException("El año debe ser 2000 o posterior.")

        if self.precio_base <= 0:
            raise DomainException("El precio debe ser mayor a cero.")

        if self.stock < 0:
            raise DomainException("El stock no puede ser negativo.")

    def tiene_stock(self):
        return self.activo and self.stock > 0

    def __str__(self):
        return self.marca + " " + self.modelo + " " + str(self.anio) + " | $" + str(self.precio_base)
