import sys
import json

from .parsers import parse_operations, serialize_results
from .calculator import CapitalGainsCalculator


def main() -> None:
    calculator = CapitalGainsCalculator()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            # empty line = end of input
            break

        raw_operations = json.loads(line)
        operations = parse_operations(raw_operations)
        results = calculator.process_operations(operations)
        output = serialize_results(results)

        print(json.dumps(output))


if __name__ == "__main__":
    main()
