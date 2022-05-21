from dataclasses import dataclass

from src.speechassistant.resources.enums import Measures


@dataclass
class Item:
    name: str
    measure: Measures
    quantity: float


@dataclass
class ShoppingList:
    sid: int
    items: list[Item]
