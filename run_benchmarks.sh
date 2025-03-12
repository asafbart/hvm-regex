#!/bin/bash

# Check if HVM is installed
if ! command -v hvm &> /dev/null; then
  echo "Error: HVM is not installed or not in PATH"
  echo "Please install HVM from https://github.com/HigherOrderCO/HVM"
  exit 1
fi

# Run basic benchmarks
echo "Running basic benchmarks..."
if [ -f "benchmarks/basic/benchmark_regex.py" ]; then
  python3 benchmarks/basic/benchmark_regex.py
else
  echo "Basic benchmark file not found."
fi

# Run optimized benchmarks
echo "Running optimized benchmarks..."
if [ -f "benchmarks/basic/optimized_benchmark.py" ]; then
  python3 benchmarks/basic/optimized_benchmark.py
else
  echo "Optimized benchmark file not found."
fi

# Run comprehensive benchmarks
echo "Running comprehensive benchmarks..."
if [ -f "benchmarks/basic/comprehensive_benchmark.py" ]; then
  python3 benchmarks/basic/comprehensive_benchmark.py
else
  echo "Comprehensive benchmark file not found."
fi

echo "Benchmarking complete."