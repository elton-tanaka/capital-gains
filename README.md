# Capital Gains CLI

This project is a command-line tool that processes stock market
operations and calculates the capital gains tax based on the rules
provided in the assignment.\
Each line of input is treated as an independent simulation and the
output is a JSON list containing the tax paid for each operation.

------------------------------------------------------------------------

## Technical and Architectural Decisions

I decided to structure the project using small, focused modules instead
of putting everything in a single script. The main goal was to make the
code easier to understand, test, and extend.

The project follows a simple separation of concerns:

-   **domain.py** contains the core data structures (`Operation`,
    `TaxResult`, and `OperationType`).\
    These types make the business rules easier to read and avoid
    reliance on raw dictionaries.

-   **calculator.py** contains the capital gains calculation logic in a
    dedicated class.\
    The class keeps internal state for weighted average, number of
    shares, and accumulated loss.\
    This keeps all business rules isolated from input/output concerns.

-   **parsers.py** handles the conversion between JSON dictionaries and
    domain objects.\
    This avoids mixing parsing logic with business logic.

-   **cli.py** is a thin wrapper responsible only for reading input from
    stdin, calling the calculator, and printing the output.

The project was also containerized using Docker so it runs consistently
regardless of environment. Tests are executed inside the same image used
to run the CLI, which ensures the code behaves the same way in all
environments.


------------------------------------------------------------------------

## How to Build and Run the Project

### Running Locally (without Docker)

Requirements: - Python 3.12 or above - pip

Install dependencies:

    pip install -r requirements.txt

Run the CLI:

    python -m capital_gains.cli

You can pipe input directly:

    echo '[{"operation":"buy","unit-cost":10.0,"quantity":1000}]' | python -m capital_gains.cli

Send an empty line to finish.

------------------------------------------------------------------------

## How to Run Using Docker

Build the Docker image:

    docker build -t capital-gains .

Run the program with input:

    echo '[{"operation":"buy","unit-cost":10.0,"quantity":1000}]' | docker run --rm -i capital-gains

Or run interactively:

    docker run --rm -it capital-gains

------------------------------------------------------------------------

## How to Run Tests

### Locally

    pytest

With coverage:

    coverage run -m pytest
    coverage report -m

### Inside Docker

    docker run --rm -it capital-gains pytest

------------------------------------------------------------------------