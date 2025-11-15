from dataclasses import dataclass
from enum import Enum


class OperationType(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Operation:
    type: OperationType
    unit_cost: float
    quantity: int


@dataclass
class TaxResult:
    tax: float