from abc import ABC, abstractmethod

class RepositoryInterface(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass
    
    @abstractmethod
    def get_by_id(self, id):
        pass
