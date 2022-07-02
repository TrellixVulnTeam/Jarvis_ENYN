from dataclasses import dataclass
from typing import Optional

from resources.enums import Measures


@dataclass
class ShoppingListItem:
    id: Optional[int]
    name: str
    measure: Measures
    quantity: float

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "measure": self.measure,
            "quantity": self.quantity,
        }
