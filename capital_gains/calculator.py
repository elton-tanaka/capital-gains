from typing import List
from .domain import Operation, OperationType, TaxResult

TAX_RATE = 0.20
TAX_FREE_THRESHOLD = 20000.0


class CapitalGainsCalculator:
    def __init__(
        self,
        tax_rate: float = TAX_RATE,
        tax_free_threshold: float = TAX_FREE_THRESHOLD,
    ) -> None:
        self.tax_rate = tax_rate
        self.tax_free_threshold = tax_free_threshold
        self._reset_state()

    def _reset_state(self) -> None:
        self.weighted_average = 0.0
        self.shares = 0               # quantity of shares
        self.accumulated_loss = 0.0

    def process_operations(self, operations: List[Operation]) -> List[TaxResult]:
        # every line of input is independent
        self._reset_state()
        results: List[TaxResult] = []

        for op in operations:
            if op.type == OperationType.BUY:
                results.append(self._handle_buy(op))
            else:
                results.append(self._handle_sell(op))

        return results

    def _handle_buy(self, op: Operation) -> TaxResult:
        # no tax here
        if self.shares == 0:
            self.weighted_average = op.unit_cost
        else:
            self.weighted_average = (
                (self.shares * self.weighted_average)
                + (op.quantity * op.unit_cost)
            ) / (self.shares + op.quantity)

        self.shares += op.quantity
        return TaxResult(tax=0.0)

    def _handle_sell(self, op: Operation) -> TaxResult:
        total_value = op.unit_cost * op.quantity
        profit = (op.unit_cost - self.weighted_average) * op.quantity
        tax = 0.0

        if total_value <= self.tax_free_threshold:
            # Operations below 20k dont get taxed
            # profit dont lower losses but losses do get added to accumulated losses
            if profit < 0:
                self.accumulated_loss += -profit
        else:
            # Operations above 20k can get taxed
            if profit > 0:
                # lower previous losses before taxing
                if self.accumulated_loss >= profit:
                    self.accumulated_loss -= profit
                    tax = 0.0
                else:
                    taxable_profit = profit - self.accumulated_loss
                    self.accumulated_loss = 0.0
                    tax = taxable_profit * self.tax_rate
            elif profit < 0:
                # losses accumulate
                self.accumulated_loss += -profit
                tax = 0.0

        self.shares -= op.quantity
        return TaxResult(tax=tax)
