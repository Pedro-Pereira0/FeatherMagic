from abc import ABC, abstractmethod

class RepositoryInterface(ABC):
    @abstractmethod
    def create(self, data):
        pass

    def search(self, query):
        pass
