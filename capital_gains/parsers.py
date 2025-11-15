from typing import Any, Dict, List
from .domain import Operation, OperationType, TaxResult


def parse_operations(raw_operations: List[Dict[str, Any]]) -> List[Operation]:
    """
    Converts the list of dicts (JSON) into a list of Operations.
    Expects the following fields: "operation", "unit-cost", "quantity".
    """
    operations: List[Operation] = []

    for item in raw_operations:
        try:
            op_type_str = item["operation"]
            unit_cost = float(item["unit-cost"])
            quantity = int(item["quantity"])
        except KeyError as e:
            raise ValueError(f"Missing field in operation: {e}") from e
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid value in operation: {item}") from e

        try:
            op_type = OperationType(op_type_str)
        except ValueError as e:
            raise ValueError(f"Unknown operation type: {op_type_str}") from e

        operations.append(
            Operation(type=op_type, unit_cost=unit_cost, quantity=quantity)
        )

    return operations


def serialize_results(results: List[TaxResult]) -> List[Dict[str, float]]:
    """
    Convert Tax Result -> list of dicts with 'tax' field, 
    ready to be serialized into JSON.
    """
    return [{"tax": round(result.tax, 2)} for result in results]
