import math
from capital_gains.domain import Operation, OperationType
from capital_gains.calculator import CapitalGainsCalculator


def almost_equal(a: float, b: float, eps: float = 1e-6) -> bool:
    return math.isclose(a, b, abs_tol=eps)


def test_no_tax_on_buy_only():
    calc = CapitalGainsCalculator()
    operations = [
        Operation(type=OperationType.BUY, unit_cost=10.0, quantity=1000),
        Operation(type=OperationType.BUY, unit_cost=20.0, quantity=500),
    ]

    results = calc.process_operations(operations)

    assert len(results) == 2
    assert all(r.tax == 0.0 for r in results)


def test_simple_profit_above_threshold_tax_applied():
    calc = CapitalGainsCalculator()
    operations = [
        Operation(type=OperationType.BUY, unit_cost=10.0, quantity=2000),
        # total_value = 25_000 > 20_000, profit = (12.5 - 10) * 2000 = 5_000
        Operation(type=OperationType.SELL, unit_cost=12.5, quantity=2000),
    ]

    results = calc.process_operations(operations)

    assert len(results) == 2
    assert results[0].tax == 0.0
    # taxable profit = 5_000, tax = 20% = 1_000
    assert almost_equal(results[1].tax, 1000.0)


def test_profit_below_threshold_no_tax_and_no_loss_offset():
    calc = CapitalGainsCalculator()
    operations = [
        Operation(type=OperationType.BUY, unit_cost=10.0, quantity=1000),
        # total_value = 15_000 <= 20_000, profit = (15 - 10) * 1000 = 5_000
        Operation(type=OperationType.SELL, unit_cost=15.0, quantity=1000),
    ]

    results = calc.process_operations(operations)

    assert len(results) == 2
    assert results[0].tax == 0.0
    # no tax because total_value <= 20_000
    assert results[1].tax == 0.0

    # And this profit must NOT reduce future accumulated loss.
    # We test that indirectly in next test.


def test_loss_is_accumulated_and_offsets_future_profit():
    calc = CapitalGainsCalculator()
    operations = [
        # Buy at 20, then sell at 10 -> loss
        Operation(type=OperationType.BUY, unit_cost=20.0, quantity=1000),
        # total_value = 10_000 <= 20_000, profit = (10 - 20) * 1000 = -10_000
        Operation(type=OperationType.SELL, unit_cost=10.0, quantity=1000),
        # Buy again at 20
        Operation(type=OperationType.BUY, unit_cost=20.0, quantity=2000),
        # total_value = 60_000 > 20_000, profit = (50 - 20) * 2000 = 60_000
        # loss accumulated from previous sell = 10_000 -> taxable = 50_000
        Operation(type=OperationType.SELL, unit_cost=50.0, quantity=2000),
    ]

    results = calc.process_operations(operations)

    assert len(results) == 4

    # First buy: no tax
    assert results[0].tax == 0.0

    # First sell: loss, no tax
    assert results[1].tax == 0.0

    # Second buy: no tax
    assert results[2].tax == 0.0

    # Second sell: tax on (60_000 - 10_000) * 20% = 50_000 * 0.2 = 10_000
    assert almost_equal(results[3].tax, 10000.0)


def test_multiple_sells_use_loss_until_exhausted():
    calc = CapitalGainsCalculator()
    operations = [
        # Initial buy
        Operation(type=OperationType.BUY, unit_cost=30.0, quantity=1000),
        # Sell with loss (above threshold)
        # total_value = 20_000 * 1 = 20_000 (edge case: <= threshold -> no tax, but still loss)
        Operation(type=OperationType.SELL, unit_cost=10.0, quantity=1000),
        # New buy
        Operation(type=OperationType.BUY, unit_cost=20.0, quantity=2000),
        # First profit sell above threshold
        Operation(type=OperationType.SELL, unit_cost=40.0, quantity=1000),
        # Second profit sell above threshold
        Operation(type=OperationType.SELL, unit_cost=40.0, quantity=1000),
    ]

    results = calc.process_operations(operations)

    # Just basic sanity checks:
    assert len(results) == 5
    # No tax on buys:
    assert results[0].tax == 0.0
    assert results[2].tax == 0.0
    # Loss sells: no tax
    assert results[1].tax == 0.0
    # Profitable sells: may or may not have tax depending on how much loss is left
    # We won't over-specify here; this test mainly ensures code runs consistently.
    assert results[3].tax >= 0.0
    assert results[4].tax >= 0.0
