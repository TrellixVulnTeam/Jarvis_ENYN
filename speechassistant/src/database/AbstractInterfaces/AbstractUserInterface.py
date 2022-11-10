from abc import ABCMeta, abstractmethod


class AbstractUserInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_user_by_alias(self, alias: str):
        ...
