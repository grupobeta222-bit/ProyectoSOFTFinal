from src.domain.entities.testimonio import Testimonio
from src.infrastructure.db_connection import get_session
from src.infrastructure.orm_models import ClienteORM, TestimonioORM


class SqliteTestimonioRepository:
    def find_visibles(self):
        session = get_session()
        try:
            registros = session.query(TestimonioORM).join(TestimonioORM.cliente).filter(
                TestimonioORM.visible.is_(True)
            ).order_by(TestimonioORM.fecha.desc()).all()
            return [
                Testimonio(
                    id=registro.id,
                    cliente_id=registro.cliente_id,
                    nombre=registro.cliente.nombre,
                    email=registro.cliente.email,
                    texto=registro.texto,
                    calificacion=registro.calificacion,
                    foto_url=registro.cliente.foto_url or "",
                    visible=registro.visible,
                    fecha=registro.fecha,
                )
                for registro in registros
            ]
        finally:
            session.close()

    def save(self, testimonio):
        session = get_session()
        try:
            cliente = session.query(ClienteORM).filter_by(id=testimonio.cliente_id).first()
            if cliente is None:
                return False
            registro = TestimonioORM(
                cliente_id=cliente.id,
                texto=testimonio.texto,
                calificacion=testimonio.calificacion,
                visible=True,
            )
            session.add(registro)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
