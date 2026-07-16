from datetime import datetime

from src.domain.entities.cotizacion import Cotizacion
from src.domain.repositories.cotizacion_repository import CotizacionRepository
from src.infrastructure.db_connection import get_session
from src.infrastructure.orm_models import ClienteORM, CotizacionORM


class SqliteCotizacionRepository(CotizacionRepository):
    def _fecha_texto(self, fecha):
        if fecha is None:
            return ""
        return fecha.strftime("%Y-%m-%dT%H:%M:%S")

    def _a_entidad(self, registro):
        cliente = registro.cliente
        return Cotizacion(
            id=registro.id,
            vehiculo_id=registro.vehiculo_id,
            plan_id=registro.plan_id,
            nombre_cliente=cliente.nombre,
            email_cliente=cliente.email,
            cedula_cliente=cliente.cedula or "",
            telefono_cliente=cliente.telefono or "",
            ciudad_cliente=cliente.ciudad or "",
            asesor_id=registro.asesor_id or 1,
            precio_vehiculo=float(registro.precio_vehiculo),
            entrada=float(registro.entrada),
            plazo_meses=registro.plazo_meses,
            tasa_anual=float(registro.tasa_anual),
            estado=registro.estado,
            fecha=self._fecha_texto(registro.fecha),
            cliente_id=registro.cliente_id,
            comision_apertura=float(registro.comision_apertura),
            fecha_cierre=self._fecha_texto(registro.fecha_cierre) or None,
        )

    def _buscar_cliente(self, session, cotizacion):
        cliente = None
        if cotizacion.cliente_id:
            cliente = session.query(ClienteORM).filter_by(id=cotizacion.cliente_id).first()
        if cliente is None and cotizacion.cedula_cliente:
            cliente = session.query(ClienteORM).filter_by(cedula=cotizacion.cedula_cliente).first()
        if cliente is None and cotizacion.email_cliente:
            cliente = session.query(ClienteORM).filter_by(email=cotizacion.email_cliente).first()
        return cliente

    def _obtener_o_crear_cliente(self, session, cotizacion):
        cliente = self._buscar_cliente(session, cotizacion)

        if cliente is None:
            cliente = ClienteORM(
                nombre=cotizacion.nombre_cliente,
                email=cotizacion.email_cliente,
                cedula=cotizacion.cedula_cliente or None,
                telefono=cotizacion.telefono_cliente or None,
                ciudad=cotizacion.ciudad_cliente or None,
            )
            session.add(cliente)
            session.flush()
        else:
            cliente.nombre = cotizacion.nombre_cliente
            cliente.email = cotizacion.email_cliente
            cliente.telefono = cotizacion.telefono_cliente or None
            cliente.ciudad = cotizacion.ciudad_cliente or None

        return cliente

    def _fecha_cotizacion(self, cotizacion):
        if not cotizacion.fecha:
            return datetime.now()
        try:
            return datetime.strptime(cotizacion.fecha, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return datetime.now()

    def _llenar_cotizacion_orm(self, registro, cotizacion, cliente_id):
        registro.cliente_id = cliente_id
        registro.vehiculo_id = cotizacion.vehiculo_id
        registro.plan_id = cotizacion.plan_id
        registro.precio_vehiculo = cotizacion.precio_vehiculo
        registro.entrada = cotizacion.entrada
        registro.plazo_meses = cotizacion.plazo_meses
        registro.tasa_anual = cotizacion.tasa_anual
        registro.cuota_mensual = cotizacion.cuota_mensual
        registro.asesor_id = cotizacion.asesor_id
        registro.estado = cotizacion.estado
        registro.comision_apertura = cotizacion.comision_apertura
        registro.fecha_cierre = self._a_datetime(cotizacion.fecha_cierre)

    def _a_datetime(self, valor):
        if not valor:
            return None
        if isinstance(valor, datetime):
            return valor
        try:
            return datetime.strptime(valor, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None

    def find_all(self):
        session = get_session()
        try:
            registros = session.query(CotizacionORM).join(CotizacionORM.cliente).order_by(CotizacionORM.fecha.desc()).all()
            cotizaciones = []
            for registro in registros:
                cotizaciones.append(self._a_entidad(registro))
            return cotizaciones
        finally:
            session.close()

    def find_by_id(self, cotizacion_id):
        session = get_session()
        try:
            registro = session.query(CotizacionORM).filter_by(id=cotizacion_id).first()
            if registro is None:
                return None
            return self._a_entidad(registro)
        finally:
            session.close()

    def find_by_cedula(self, cedula):
        session = get_session()
        try:
            registros = session.query(CotizacionORM).join(CotizacionORM.cliente).filter(ClienteORM.cedula == cedula).order_by(CotizacionORM.fecha.desc()).all()
            cotizaciones = []
            for registro in registros:
                cotizaciones.append(self._a_entidad(registro))
            return cotizaciones
        finally:
            session.close()

    def save(self, cotizacion):
        session = get_session()
        try:
            cliente = self._obtener_o_crear_cliente(session, cotizacion)
            registro = session.query(CotizacionORM).filter_by(id=cotizacion.id).first()

            if registro is None:
                registro = CotizacionORM(id=cotizacion.id, fecha=self._fecha_cotizacion(cotizacion))
                session.add(registro)

            self._llenar_cotizacion_orm(registro, cotizacion, cliente.id)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update_estado(self, cotizacion_id, nuevo_estado, fecha_cierre=None):
        session = get_session()
        try:
            registro = session.query(CotizacionORM).filter_by(id=cotizacion_id).first()
            if registro is None:
                return False
            registro.estado = nuevo_estado
            registro.fecha_cierre = self._a_datetime(fecha_cierre)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
