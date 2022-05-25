from dataclasses import dataclass
from typing import Optional

from src.speechassistant.resources.enums import Measures


@dataclass
class ShoppingListItem:
    id: Optional[int]
    name: str
    measure: Measures
    quantity: float
