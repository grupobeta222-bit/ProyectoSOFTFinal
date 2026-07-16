from enum import Enum

from src.domain.exceptions.domain_exception import DomainException


class RolUsuario(str, Enum):
    GERENTE = "gerente"
    ASESOR = "asesor"


class Usuario:
    def __init__(self, id, nombre, email, password_hash, rol,
                 activo=True, especialidad="", rating=0.0, foto_url=""):
        if not nombre or not email or "@" not in email:
            raise DomainException("Datos de usuario invalidos.")
        if rol not in [item.value for item in RolUsuario]:
            raise DomainException("Rol de usuario invalido.")
        self.id = id
        self.nombre = nombre
        self.email = email.lower().strip()
        self.password_hash = password_hash
        self.rol = rol
        self.activo = bool(activo)
        self.especialidad = especialidad
        self.rating = float(rating or 0)
        self.foto_url = foto_url

    def datos_sesion(self):
        return {
            "rol": self.rol,
            "nombre": self.nombre,
            "asesor_id": self.id if self.rol == RolUsuario.ASESOR.value else None,
        }
