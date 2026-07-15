from abc import ABC, abstractmethod


class PlanRepository(ABC):

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, plan_id):
        pass

    @abstractmethod
    def save(self, plan):
        pass

    @abstractmethod
    def update(self, plan):
        pass

    @abstractmethod
    def delete(self, plan_id):
        pass
