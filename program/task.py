from abc import ABC, abstractmethod, abstractproperty


class Param:
    pass


class Task(ABC):

    @property
    @abstractproperty
    def param(self):
        return Param()