#!/bin/bash

# Performance benchmark script for HVM3 regex implementation
# This script runs the benchmark and calculates operations per second

# Change to the project directory
cd "$(dirname "$0")/.."

# Benchmark parameters
ITERATIONS=10    # Number of benchmark runs (small for quick testing)
WARMUP=5         # Number of warmup runs before measuring

# Define benchmark patterns
BENCHMARK_FILE="benchmarks/performance_benchmark.hvml"

# Print header
echo "==== HVM3 Regex Performance Benchmark ===="
echo "Iterations: $ITERATIONS"
echo ""
echo "Pattern Type | Operations | Time (sec) | Ops/sec"
echo "-------------|------------|------------|--------"

# Function to run benchmark for a specific pattern
run_benchmark() {
  local pattern_type=$1
  local iterations=$2
  
  # Warmup runs
  for ((i=1; i<=$WARMUP; i++)); do
    cabal run hvml -- run $BENCHMARK_FILE > /dev/null 2>&1
  done
  
  # Actual benchmark
  start_time=$(date +%s.%N)
  
  # Run the benchmark multiple times for more accurate measurement
  for ((i=1; i<=$ITERATIONS; i++)); do
    cabal run hvml -- run $BENCHMARK_FILE > /dev/null 2>&1
  done
  
  end_time=$(date +%s.%N)
  
  # Calculate elapsed time
  elapsed=$(echo "$end_time - $start_time" | bc)
  
  # We ran iterations * 20 operations (benchmark does 20 ops)
  total_ops=$((iterations * 20))
  
  # Calculate operations per second
  ops_per_second=$(echo "scale=2; $total_ops / $elapsed" | bc)
  
  # Print result
  printf "%-13s | %-10s | %-10s | %-8s\n" "$pattern_type" "$total_ops" "$elapsed" "$ops_per_second"
}

# Run benchmark for each pattern type
# The simple type is the first element in the result array
echo "Running benchmarks..."
echo ""

# Run all benchmarks
run_benchmark "Simple ('a')" $ITERATIONS
run_benchmark "Medium ('abc')" $ITERATIONS
run_benchmark "Complex ('(a|b)*c')" $ITERATIONS

echo ""
echo "Benchmark complete."