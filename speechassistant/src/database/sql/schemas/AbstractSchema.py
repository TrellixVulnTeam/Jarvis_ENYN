from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

Model = TypeVar("Model")
Schema = TypeVar("Schema")


class AbstractSchema(metaclass=ABCMeta, Generic[Model, Schema]):

    @abstractmethod
    def to_model(self, **kwargs) -> Model:
        ...

    @abstractmethod
    @staticmethod
    def from_model(model: Model, **kwargs) -> Schema:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...
