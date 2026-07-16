from src.domain.entities.cliente import Cliente
from src.domain.repositories.cliente_repository import ClienteRepository
from src.infrastructure.db_connection import get_session
from src.infrastructure.orm_models import ClienteORM


class SqliteClienteRepository(ClienteRepository):
    def _a_entidad(self, registro):
        return Cliente(
            nombre=registro.nombre,
            email=registro.email or "",
            cedula=registro.cedula or "",
            telefono=registro.telefono or "",
            ciudad=registro.ciudad or "",
            id=registro.id,
            foto_url=registro.foto_url or "",
        )

    def save(self, cliente, password_hash=None):
        session = get_session()
        try:
            registro = ClienteORM(
                nombre=cliente.nombre,
                email=cliente.email,
                cedula=cliente.cedula or None,
                telefono=cliente.telefono or None,
                ciudad=cliente.ciudad or None,
                foto_url=cliente.foto_url or None,
                password_hash=password_hash,
            )
            session.add(registro)
            session.commit()
            return registro.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def save_or_update(self, cliente, password_hash=None):
        session = get_session()
        try:
            registro = None
            if cliente.id:
                registro = session.query(ClienteORM).filter_by(id=cliente.id).first()
            if cliente.cedula:
                registro = registro or session.query(ClienteORM).filter_by(cedula=cliente.cedula).first()
            if cliente.email:
                registro = registro or session.query(ClienteORM).filter_by(email=cliente.email).first()

            if registro is None:
                registro = ClienteORM(cedula=cliente.cedula or None)
                session.add(registro)

            registro.nombre = cliente.nombre
            registro.email = cliente.email
            registro.telefono = cliente.telefono or None
            registro.ciudad = cliente.ciudad or None
            registro.foto_url = cliente.foto_url or None
            if password_hash:
                registro.password_hash = password_hash
            session.commit()
            return registro.id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def find_all(self):
        session = get_session()
        try:
            registros = session.query(ClienteORM).order_by(ClienteORM.nombre).all()
            clientes = []
            for registro in registros:
                clientes.append(self._a_entidad(registro))
            return clientes
        finally:
            session.close()

    def find_by_id(self, cliente_id):
        session = get_session()
        try:
            registro = session.query(ClienteORM).filter_by(id=cliente_id).first()
            if registro is None:
                return None
            return self._a_entidad(registro)
        finally:
            session.close()

    def find_by_cedula(self, cedula):
        session = get_session()
        try:
            registro = session.query(ClienteORM).filter_by(cedula=cedula).first()
            if registro is None:
                return None
            return self._a_entidad(registro)
        finally:
            session.close()

    def find_by_email(self, email):
        session = get_session()
        try:
            registro = session.query(ClienteORM).filter_by(email=email).first()
            if registro is None:
                return None
            return self._a_entidad(registro)
        finally:
            session.close()

    def obtener_acceso(self, email):
        session = get_session()
        try:
            registro = session.query(ClienteORM).filter_by(email=email).first()
            if registro is None:
                return None
            return self._a_entidad(registro), registro.password_hash
        finally:
            session.close()

    def actualizar_perfil(self, email, cliente, password_hash=None):
        session = get_session()
        try:
            registro = session.query(ClienteORM).filter_by(email=email).first()
            if registro is None:
                return None
            registro.nombre = cliente.nombre
            registro.cedula = cliente.cedula or None
            registro.telefono = cliente.telefono or None
            registro.ciudad = cliente.ciudad or None
            registro.foto_url = cliente.foto_url or None
            if password_hash:
                registro.password_hash = password_hash
            session.commit()
            return self._a_entidad(registro)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
