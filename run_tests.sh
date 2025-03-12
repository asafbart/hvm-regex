#!/bin/bash

# Check if HVM is installed
if ! command -v hvm &> /dev/null; then
  echo "Error: HVM is not installed or not in PATH"
  echo "Please install HVM from https://github.com/HigherOrderCO/HVM"
  exit 1
fi

# Run HVML tests
echo "Running HVML tests..."
for test_file in tests/unit/*.hvml; do
  if [ -f "$test_file" ]; then
    echo "Running $test_file"
    hvm run "$test_file"
  fi
done

# Run Python tests if Python is available
if command -v python3 &> /dev/null; then
  echo "Running Python tests..."
  for test_file in tests/unit/test_*.py; do
    if [ -f "$test_file" ]; then
      echo "Running $test_file"
      python3 "$test_file"
    fi
  done
else
  echo "Python not found. Skipping Python tests."
fi

echo "Testing complete."