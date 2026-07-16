from src.domain.entities.usuario import Usuario
from src.infrastructure.db_connection import get_session
from src.infrastructure.orm_models import UsuarioORM


class SqliteUsuarioRepository:
    def _a_entidad(self, registro):
        return Usuario(
            id=registro.id,
            nombre=registro.nombre,
            email=registro.email,
            password_hash=registro.password_hash,
            rol=registro.rol,
            activo=registro.activo,
            especialidad=registro.especialidad or "",
            rating=float(registro.rating or 0),
            foto_url=registro.foto_url or "",
        )

    def find_by_email(self, email):
        session = get_session()
        try:
            registro = session.query(UsuarioORM).filter_by(email=email).first()
            if registro is None:
                return None
            return self._a_entidad(registro), registro.password_hash
        finally:
            session.close()

    def find_by_id(self, usuario_id):
        session = get_session()
        try:
            registro = session.query(UsuarioORM).filter_by(id=usuario_id).first()
            return self._a_entidad(registro) if registro else None
        finally:
            session.close()

    def find_asesores(self):
        session = get_session()
        try:
            registros = session.query(UsuarioORM).filter_by(rol="asesor", activo=True).order_by(UsuarioORM.id).all()
            return [self._a_entidad(registro) for registro in registros]
        finally:
            session.close()
