from src.domain.entities.cliente import Cliente
from src.domain.exceptions.domain_exception import DomainException
from src.infrastructure.security import hash_password, verify_password


class ClienteService:
    def __init__(self, cliente_repo, cotizacion_repo):
        self.cliente_repo = cliente_repo
        self.cotizacion_repo = cotizacion_repo

    def registrar(self, nombre, email, cedula, telefono, password):
        email = (email or "").lower().strip()
        if self.cliente_repo.find_by_email(email):
            raise DomainException("El correo ya está registrado.")
        cliente = Cliente(nombre, email, cedula or "", telefono or "", "")
        cliente.id = self.cliente_repo.save(cliente, hash_password(password))
        return cliente

    def autenticar(self, email, password):
        resultado = self.cliente_repo.obtener_acceso((email or "").lower().strip())
        if resultado is None:
            return None
        cliente, password_hash = resultado
        if not verify_password(password, password_hash):
            return None
        return self._datos(cliente)

    def actualizar_perfil(self, email, nombre, telefono, cedula, password=""):
        actual = self.cliente_repo.find_by_email(email)
        if actual is None:
            raise DomainException("Cliente no encontrado.")
        cliente = Cliente(
            nombre, email, cedula or "", telefono or "", actual.ciudad,
            id=actual.id, foto_url=actual.foto_url,
        )
        nuevo_hash = hash_password(password) if password else None
        guardado = self.cliente_repo.actualizar_perfil(email, cliente, nuevo_hash)
        return self._datos(guardado)

    def cotizaciones_por_email(self, email):
        cliente = self.cliente_repo.find_by_email(email)
        if cliente is None or not cliente.cedula:
            return []
        return self.cotizacion_repo.find_by_cedula(cliente.cedula)

    @staticmethod
    def _datos(cliente):
        return {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "email": cliente.email,
            "cedula": cliente.cedula,
            "telefono": cliente.telefono,
            "foto_url": cliente.foto_url,
        }
