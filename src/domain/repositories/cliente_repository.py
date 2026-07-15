from abc import ABC, abstractmethod


class ClienteRepository(ABC):

    @abstractmethod
    def save(self, cliente):
        pass

    @abstractmethod
    def save_or_update(self, cliente):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, cliente_id):
        pass

    @abstractmethod
    def find_by_cedula(self, cedula):
        pass

    @abstractmethod
    def find_by_email(self, email):
        pass
