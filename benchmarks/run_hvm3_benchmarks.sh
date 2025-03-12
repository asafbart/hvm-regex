#!/bin/bash

# HVM3 Regex Performance Benchmark Script
# This script runs performance tests for the HVM3-compatible regex implementation

# Set default parameters
TEST_TYPE="all"
ITERATIONS=5
OUTPUT_DIR="results"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --type)
      TEST_TYPE="$2"
      shift 2
      ;;
    --iterations)
      ITERATIONS="$2"
      shift 2
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--type all|pattern-complexity|input-size|features|pathological] [--iterations N] [--output DIR]"
      exit 1
      ;;
  esac
done

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to run a benchmark test
run_benchmark() {
  local test_name="$1"
  local test_file="$2"
  local result_file="$OUTPUT_DIR/${test_name}.csv"
  
  echo "Running benchmark: $test_name"
  echo "Iterations: $ITERATIONS"
  
  echo "test,iteration,time_ms,memory_kb" > "$result_file"
  
  for i in $(seq 1 $ITERATIONS); do
    echo "  Iteration $i/$ITERATIONS..."
    
    # Time the execution
    start_time=$(date +%s%N)
    hvm run "$test_file" > /dev/null 2>&1
    end_time=$(date +%s%N)
    
    # Calculate time in milliseconds
    time_ms=$(( (end_time - start_time) / 1000000 ))
    
    # Get memory usage (simplified, in a real scenario this would capture actual memory usage)
    memory_kb=0  # Placeholder, would need a proper way to measure memory
    
    # Record result
    echo "$test_name,$i,$time_ms,$memory_kb" >> "$result_file"
  done
  
  # Calculate and display average
  avg_time=$(awk -F, '{sum+=$3} END {print sum/NR}' "$result_file" | tail -n +2)
  echo "  Average execution time: ${avg_time}ms"
}

# Run pattern complexity benchmarks
run_pattern_complexity_benchmarks() {
  echo "=== PATTERN COMPLEXITY BENCHMARKS ==="
  
  # Simple patterns
  run_benchmark "pattern_simple" "../tests/unit/regex_hvm3_simple.hvml"
  
  # Medium complexity patterns
  run_benchmark "pattern_medium" "../tests/unit/regex_hvm3_test.hvml"
  
  # Complex patterns
  run_benchmark "pattern_complex" "../tests/unit/test_regex_hvm3.hvml"
  
  # Very complex patterns
  run_benchmark "pattern_very_complex" "../tests/unit/test_regex_hvm3_complete.hvml"
}

# Run input size benchmarks
run_input_size_benchmarks() {
  echo "=== INPUT SIZE BENCHMARKS ==="
  
  # These benchmarks would involve creating dedicated test files for different input sizes
  # Placeholder for now, would need actual test files

  echo "Input size benchmarks - To be implemented"
  # Uncomment and modify once the test files are created
  # run_benchmark "input_tiny" "../benchmarks/input_tiny.hvml"
  # run_benchmark "input_small" "../benchmarks/input_small.hvml"
  # run_benchmark "input_medium" "../benchmarks/input_medium.hvml"
  # run_benchmark "input_large" "../benchmarks/input_large.hvml"
}

# Run feature-specific benchmarks
run_feature_benchmarks() {
  echo "=== FEATURE-SPECIFIC BENCHMARKS ==="
  
  # These benchmarks would involve creating dedicated test files for different regex features
  # Placeholder for now, would need actual test files

  echo "Feature-specific benchmarks - To be implemented"
  # Uncomment and modify once the test files are created
  # run_benchmark "feature_alternation" "../benchmarks/feature_alternation.hvml"
  # run_benchmark "feature_repetition" "../benchmarks/feature_repetition.hvml"
  # run_benchmark "feature_charclass" "../benchmarks/feature_charclass.hvml"
}

# Run pathological case benchmarks
run_pathological_benchmarks() {
  echo "=== PATHOLOGICAL CASE BENCHMARKS ==="
  
  # These benchmarks would involve creating dedicated test files for pathological regex patterns
  # Placeholder for now, would need actual test files

  echo "Pathological case benchmarks - To be implemented"
  # Uncomment and modify once the test files are created
  # run_benchmark "pathological_nested" "../benchmarks/pathological_nested.hvml"
  # run_benchmark "pathological_overlapping" "../benchmarks/pathological_overlapping.hvml"
  # run_benchmark "pathological_greedy" "../benchmarks/pathological_greedy.hvml"
}

# Generate a summary report
generate_report() {
  echo "=== GENERATING BENCHMARK REPORT ==="
  
  report_file="$OUTPUT_DIR/benchmark_report.md"
  
  echo "# HVM3 Regex Benchmark Results" > "$report_file"
  echo "" >> "$report_file"
  echo "Benchmark run on: $(date)" >> "$report_file"
  echo "Iterations per test: $ITERATIONS" >> "$report_file"
  echo "" >> "$report_file"
  
  # Generate pattern complexity summary
  if [[ -f "$OUTPUT_DIR/pattern_simple.csv" ]]; then
    echo "## Pattern Complexity Results" >> "$report_file"
    echo "" >> "$report_file"
    echo "| Pattern Type | Average Time (ms) |" >> "$report_file"
    echo "|--------------|-------------------|" >> "$report_file"
    
    simple_avg=$(awk -F, '{sum+=$3} END {print sum/NR}' "$OUTPUT_DIR/pattern_simple.csv" | tail -n +2)
    echo "| Simple | $simple_avg |" >> "$report_file"
    
    if [[ -f "$OUTPUT_DIR/pattern_medium.csv" ]]; then
      medium_avg=$(awk -F, '{sum+=$3} END {print sum/NR}' "$OUTPUT_DIR/pattern_medium.csv" | tail -n +2)
      echo "| Medium | $medium_avg |" >> "$report_file"
    fi
    
    if [[ -f "$OUTPUT_DIR/pattern_complex.csv" ]]; then
      complex_avg=$(awk -F, '{sum+=$3} END {print sum/NR}' "$OUTPUT_DIR/pattern_complex.csv" | tail -n +2)
      echo "| Complex | $complex_avg |" >> "$report_file"
    fi
    
    if [[ -f "$OUTPUT_DIR/pattern_very_complex.csv" ]]; then
      very_complex_avg=$(awk -F, '{sum+=$3} END {print sum/NR}' "$OUTPUT_DIR/pattern_very_complex.csv" | tail -n +2)
      echo "| Very Complex | $very_complex_avg |" >> "$report_file"
    fi
    
    echo "" >> "$report_file"
  fi
  
  # Add other sections for input size, features, etc.
  # ...
  
  echo "Benchmark report generated: $report_file"
}

# Run benchmarks based on the test type
case $TEST_TYPE in
  "all")
    run_pattern_complexity_benchmarks
    run_input_size_benchmarks
    run_feature_benchmarks
    run_pathological_benchmarks
    ;;
  "pattern-complexity")
    run_pattern_complexity_benchmarks
    ;;
  "input-size")
    run_input_size_benchmarks
    ;;
  "features")
    run_feature_benchmarks
    ;;
  "pathological")
    run_pathological_benchmarks
    ;;
  *)
    echo "Unknown test type: $TEST_TYPE"
    echo "Usage: $0 [--type all|pattern-complexity|input-size|features|pathological] [--iterations N] [--output DIR]"
    exit 1
    ;;
esac

# Generate the final report
generate_report

echo "Benchmarks completed. Results are in the $OUTPUT_DIR directory."