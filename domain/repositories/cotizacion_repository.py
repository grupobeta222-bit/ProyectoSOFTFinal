from abc import ABC, abstractmethod


class CotizacionRepository(ABC):

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, cotizacion_id):
        pass

    @abstractmethod
    def find_by_cedula(self, cedula):
        pass

    @abstractmethod
    def save(self, cotizacion):
        pass

    @abstractmethod
    def update_estado(self, cotizacion_id, nuevo_estado, fecha_cierre=None):
        pass
