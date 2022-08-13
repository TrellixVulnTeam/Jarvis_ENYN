from enum import Enum


class OutputTypes(Enum):
    INT = 1
    FLOAT = 2
    STRING = 3
    ARRAY = 4
    DICT = 5
    TUPLE = 6


class Measures(Enum):
    mg: 1
    g: 2
    kg: 3
    ml: 4
    l: 5
