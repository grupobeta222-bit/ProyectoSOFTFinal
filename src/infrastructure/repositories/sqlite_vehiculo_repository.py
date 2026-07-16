from src.domain.entities.vehiculo import Vehiculo
from src.domain.repositories.vehiculo_repository import VehiculoRepository
from src.infrastructure.db_connection import get_session
from src.infrastructure.orm_models import VehiculoORM


class SqliteVehiculoRepository(VehiculoRepository):
    def _a_entidad(self, registro):
        return Vehiculo(
            id=registro.id,
            marca=registro.marca,
            modelo=registro.modelo,
            anio=registro.anio,
            precio_base=float(registro.precio_base),
            stock=registro.stock,
            motor=registro.motor or "N/D",
            transmision=registro.transmision or "N/D",
            combustible=registro.combustible or "Gasolina",
            activo=registro.activo,
        )

    def _a_orm(self, vehiculo):
        return VehiculoORM(
            id=vehiculo.id,
            marca=vehiculo.marca,
            modelo=vehiculo.modelo,
            anio=vehiculo.anio,
            precio_base=vehiculo.precio_base,
            stock=vehiculo.stock,
            motor=vehiculo.motor,
            transmision=vehiculo.transmision,
            combustible=vehiculo.combustible,
            activo=vehiculo.activo,
        )

    def find_all(self):
        session = get_session()
        try:
            registros = session.query(VehiculoORM).order_by(VehiculoORM.id).all()
            vehiculos = []
            for registro in registros:
                vehiculos.append(self._a_entidad(registro))
            return vehiculos
        finally:
            session.close()

    def find_by_id(self, vehiculo_id):
        session = get_session()
        try:
            registro = session.query(VehiculoORM).filter_by(id=vehiculo_id).first()
            if registro is None:
                return None
            return self._a_entidad(registro)
        finally:
            session.close()

    def save(self, vehiculo):
        session = get_session()
        try:
            session.merge(self._a_orm(vehiculo))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update(self, vehiculo):
        self.save(vehiculo)

    def delete(self, vehiculo_id):
        session = get_session()
        try:
            registro = session.query(VehiculoORM).filter_by(id=vehiculo_id).first()
            if registro is None:
                return False
            session.delete(registro)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
