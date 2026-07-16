from src.domain.entities.plan_financiamiento import PlanFinanciamiento
from src.domain.repositories.plan_repository import PlanRepository
from src.infrastructure.db_connection import get_session
from src.infrastructure.orm_models import PlanFinanciamientoORM


class SqlitePlanRepository(PlanRepository):
    def _a_entidad(self, registro):
        return PlanFinanciamiento(
            id=registro.id,
            nombre=registro.nombre,
            entrada_minima_porcentaje=float(registro.entrada_minima_porcentaje),
            tasa_anual=float(registro.tasa_anual),
            plazos_disponibles=list(registro.plazos_disponibles),
            comision_apertura=float(registro.comision_apertura),
            activo=registro.activo,
        )

    def _a_orm(self, plan):
        return PlanFinanciamientoORM(
            id=plan.id,
            nombre=plan.nombre,
            entrada_minima_porcentaje=plan.entrada_minima_porcentaje,
            tasa_anual=plan.tasa_anual,
            plazos_disponibles=plan.plazos_disponibles,
            comision_apertura=plan.comision_apertura,
            activo=plan.activo,
        )

    def find_all(self):
        session = get_session()
        try:
            registros = session.query(PlanFinanciamientoORM).order_by(PlanFinanciamientoORM.id).all()
            planes = []
            for registro in registros:
                planes.append(self._a_entidad(registro))
            return planes
        finally:
            session.close()

    def find_by_id(self, plan_id):
        session = get_session()
        try:
            registro = session.query(PlanFinanciamientoORM).filter_by(id=plan_id).first()
            if registro is None:
                return None
            return self._a_entidad(registro)
        finally:
            session.close()

    def save(self, plan):
        session = get_session()
        try:
            session.merge(self._a_orm(plan))
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update(self, plan):
        self.save(plan)

    def delete(self, plan_id):
        session = get_session()
        try:
            registro = session.query(PlanFinanciamientoORM).filter_by(id=plan_id).first()
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
