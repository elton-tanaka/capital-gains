# capital-gains

# Build
docker compose build

# Run with input from echo
echo '[{"operation":"buy","unit-cost":10.0,"quantity":1000}]' \
  | docker compose run --rm capital-gains

# Run with input file
docker compose run --rm capital-gains < input.txt