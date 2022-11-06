from src.database.sql.operations.AbstractInterface import AbstractInterface


class RoutineInterface(AbstractInterface):
    @staticmethod
    def load_by_id(id_value: str) -> RoutineSchema:
        pass

    @staticmethod
    def load_all() -> list[RoutineSchema]:
        pass
