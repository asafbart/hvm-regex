#!/bin/bash

# Performance benchmark script for HVM3 regex implementation using hardcoded patterns
# This script runs benchmarks for 30 seconds with proper warmup and calculates operations per second

# Change to the project directory
cd "$(dirname "$0")/.."

# Benchmark parameters
WARMUP_TIME=10      # Warmup time in seconds
MEASURE_TIME=30     # Measurement time in seconds
BENCHMARK_FILE="benchmarks/hardcoded_benchmark.hvml"

# Print header
echo "==== HVM3 Regex Performance Benchmark ===="
echo "Using fixed hardcoded patterns"
echo "Warmup: $WARMUP_TIME seconds"
echo "Measurement: $MEASURE_TIME seconds"
echo ""

# Function to run benchmark
run_benchmark() {
  echo "Running benchmark..."
  
  # Initial cold run
  echo "  Initial cold run..."
  cabal run hvml -- run $BENCHMARK_FILE > /dev/null 2>&1
  
  # Warmup phase
  echo "  Warming up for $WARMUP_TIME seconds..."
  end_warmup=$(($(date +%s) + WARMUP_TIME))
  warmup_count=0
  
  while [ $(date +%s) -lt $end_warmup ]; do
    cabal run hvml -- run $BENCHMARK_FILE > /dev/null 2>&1
    warmup_count=$((warmup_count + 1))
  done
  
  echo "  Warmup complete ($warmup_count runs)"
  
  # Measurement phase
  echo "  Measuring for $MEASURE_TIME seconds..."
  start_time=$(date +%s.%N)
  end_time=$(($(date +%s) + MEASURE_TIME))
  measure_count=0
  
  while [ $(date +%s) -lt $end_time ]; do
    output=$(cabal run hvml -- run $BENCHMARK_FILE 2>/dev/null)
    if [[ $output =~ [0-9]+ ]]; then
      operations_per_run=${BASH_REMATCH[0]}
    else
      operations_per_run=250  # Default if parsing fails (hardcoded benchmark does 250 ops)
    fi
    total_ops=$((total_ops + operations_per_run))
    measure_count=$((measure_count + 1))
  done
  
  actual_end_time=$(date +%s.%N)
  
  # Calculate actual elapsed time (in seconds with decimal precision)
  elapsed=$(echo "$actual_end_time - $start_time" | bc)
  
  # Calculate operations per second
  ops_per_second=$(echo "scale=2; ($measure_count * 250) / $elapsed" | bc)
  
  echo ""
  echo "=== Results ==="
  echo "Measurement runs: $measure_count"
  echo "Total operations: $(($measure_count * 250))"
  echo "Elapsed time: ${elapsed} seconds"
  echo "Operations per second: ${ops_per_second}"
}

# Run the benchmark
run_benchmark