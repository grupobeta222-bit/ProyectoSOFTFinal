from src.domain.exceptions.domain_exception import DomainException


class Cliente:

    def __init__(self, nombre, email, cedula="", telefono="", ciudad="",
                 id=None, foto_url=""):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.cedula = cedula
        self.telefono = telefono
        self.ciudad = ciudad
        self.foto_url = foto_url
        self._validar()

    def _validar(self):
        if not self.nombre or len(self.nombre.strip()) < 3:
            raise DomainException("Nombre invalido.")

        if not self.email or "@" not in self.email:
            raise DomainException("Correo invalido.")

        if self.cedula:
            if not self.cedula.isdigit() or len(self.cedula) != 10:
                raise DomainException("Cedula invalida. Debe tener 10 digitos.")

        if self.telefono:
            tel = self.telefono.replace("-", "").replace(" ", "")
            if not tel.isdigit() or len(tel) < 7:
                raise DomainException("Telefono invalido.")

    def __str__(self):
        return self.nombre + " (" + self.email + ")"
