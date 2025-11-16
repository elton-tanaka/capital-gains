import pytest

from capital_gains.parsers import parse_operations, serialize_results
from capital_gains.domain import OperationType, TaxResult


def test_parse_operations_valid_input():
    raw = [
        {"operation": "buy", "unit-cost": 10.0, "quantity": 100},
        {"operation": "sell", "unit-cost": 20.0, "quantity": 50},
    ]

    ops = parse_operations(raw)

    assert len(ops) == 2

    assert ops[0].type == OperationType.BUY
    assert ops[0].unit_cost == 10.0
    assert ops[0].quantity == 100

    assert ops[1].type == OperationType.SELL
    assert ops[1].unit_cost == 20.0
    assert ops[1].quantity == 50


def test_parse_operations_missing_field_raises():
    raw = [
        {"operation": "buy", "unit-cost": 10.0},  # missing quantity
    ]

    with pytest.raises(ValueError) as exc:
        parse_operations(raw)

    assert "Missing field" in str(exc.value)


def test_parse_operations_invalid_type_value_raises():
    raw = [
        {"operation": "buy", "unit-cost": "not-a-number", "quantity": 100},
    ]

    with pytest.raises(ValueError) as exc:
        parse_operations(raw)

    assert "Invalid value" in str(exc.value)


def test_parse_operations_unknown_operation_type_raises():
    raw = [
        {"operation": "hold", "unit-cost": 10.0, "quantity": 100},
    ]

    with pytest.raises(ValueError) as exc:
        parse_operations(raw)

    assert "Unknown operation type" in str(exc.value)


def test_serialize_results_rounds_tax_to_two_decimals():
    results = [
        TaxResult(tax=0.0),
        TaxResult(tax=1234.5678),
        TaxResult(tax=10.1),
    ]

    serialized = serialize_results(results)

    assert serialized == [
        {"tax": 0.0},
        {"tax": 1234.57},
        {"tax": 10.1},  # Python keeps one decimal if second is zero
    ]
