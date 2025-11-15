import sys
import json
from .calculator import process_operations


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            # Empty line = end of input according to spec
            break

        operations = json.loads(line)
        taxes = process_operations(operations)
        # taxes must be a list of dicts: [{ "tax": 0.0 }, ...]
        print(json.dumps(taxes))


if __name__ == "__main__":
    main()
