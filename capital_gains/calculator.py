from typing import List, Dict, Any

def process_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    taxes: List[Dict[str, float]] = []

    # Estado interno da simulação (por linha de input)
    wa = 0.0                 # média ponderada de compra
    qty_shares = 0           # quantidade total de ações em carteira
    accumulated_loss = 0.0   # prejuízo acumulado (para abater lucros futuros)

    for op in operations:
        op_type = op["operation"]
        unit_cost = op["unit-cost"]
        quantity = op["quantity"]

        if op_type == "buy":
            # Nenhum imposto em compra
            taxes.append({"tax": 0.0})

            # Recalcula média ponderada:
            # nova_media = ((qt_atual * media_atual) + (qt_compra * preco_compra)) / (qt_atual + qt_compra)
            if qty_shares == 0:
                wa = unit_cost
            else:
                wa = ((qty_shares * wa) + (quantity * unit_cost)) / (qty_shares + quantity)

            qty_shares += quantity

        elif op_type == "sell":
            # Valor total da operação
            total_value = unit_cost * quantity

            # Lucro (ou prejuízo) da operação em relação à média ponderada
            # lucro > 0  => lucro
            # lucro < 0  => prejuízo
            profit = (unit_cost - wa) * quantity

            tax = 0.0

            if total_value <= 20000:
                # Regra: se valor total da operação <= 20k
                # - não paga imposto
                # - se deu lucro, NÃO desconta dos prejuízos acumulados
                # - se deu prejuízo, acumula para abater lucros futuros
                if profit < 0:
                    accumulated_loss += -profit  # adiciona prejuízo
                tax = 0.0
            else:
                # Valor da operação > 20k: aqui pode haver imposto
                if profit > 0:
                    # Antes de calcular imposto, abate prejuízos acumulados
                    if accumulated_loss >= profit:
                        # Prejuízo cobre todo o lucro -> ainda não paga imposto
                        accumulated_loss -= profit
                        tax = 0.0
                    else:
                        # Parte do lucro vira lucro tributável
                        taxable_profit = profit - accumulated_loss
                        accumulated_loss = 0.0
                        tax = taxable_profit * 0.20  # 20% sobre o lucro
                elif profit < 0:
                    # Prejuízo: acumula
                    accumulated_loss += -profit
                    tax = 0.0
                else:
                    # lucro == 0 -> sem imposto, sem mexer no prejuízo
                    tax = 0.0

            qty_shares -= quantity

            # Se quiser arredondar o imposto para 2 casas:
            # tax = round(tax, 2)
            taxes.append({"tax": tax})

    return taxes