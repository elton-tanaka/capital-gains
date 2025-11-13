from typing import List, Dict, Any


def process_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """
    operations: list of dicts like:
      {"operation": "buy"|"sell", "unit-cost": float, "quantity": int}

    returns: list of dicts:
      [{"tax": float}, ...]
    """
    # TODO: implement Nubank "Ganho de Capital" rules here
    taxes: List[Dict[str, float]] = []

    # placeholder: no tax on anything yet
    for _op in operations:
        taxes.append({"tax": 0.0})

    return taxes
