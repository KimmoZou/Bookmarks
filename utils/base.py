from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def start(self, signal, actions):
        pass
