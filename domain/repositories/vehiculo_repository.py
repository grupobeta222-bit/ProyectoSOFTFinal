from abc import ABC, abstractmethod


class VehiculoRepository(ABC):

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, vehiculo_id):
        pass

    @abstractmethod
    def save(self, vehiculo):
        pass

    @abstractmethod
    def update(self, vehiculo):
        pass

    @abstractmethod
    def delete(self, vehiculo_id):
        pass
