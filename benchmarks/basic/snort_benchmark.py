#!/usr/bin/env python3
"""
Benchmark for the Snort pattern matcher implementation in HVM.
This compares performance of HVM multi-pattern matching against sequential matching.
"""

import os
import subprocess
import time
import re
import sys
from datetime import datetime
import platform

# Path to HVM executable
HVM_PATH = "/Users/asafbartov/claudeprojects/hvmsnort/HVM3/dist-newstyle/build/x86_64-osx/ghc-9.12.1/HVM3-0.1.0.0/x/hvml/opt/build/hvml/hvml"

# Number of patterns to test with
# Note: Uncomment the larger counts when testing with more patterns
PATTERN_COUNTS = [5, 10, 25]
# PATTERN_COUNTS = [5, 10, 25, 50, 100]  # For more extensive testing

# Benchmark configuration
WARMUP_TIME = 2.0       # Warmup time in seconds
ITERATIONS = 5          # Number of iterations for each test after warmup
TIMEOUT = 120           # Timeout in seconds for each benchmark run

def create_sequential_benchmark(patterns, traffic, pattern_count):
    """Create a benchmark file that runs patterns sequentially"""
    
    # Limit patterns to the requested count
    pattern_subset = f"(slice @snort_patterns 0 {pattern_count})"
    
    benchmark_code = f"""// Sequential pattern matching benchmark
@include "multi_pattern_impl.hvml"

// Sequential matching function
@match_sequential(patterns, traffic) =
  @match_sequential_iter(patterns, traffic, 0, (len patterns), [])

// Iterator for sequential pattern matching
@match_sequential_iter(patterns, traffic, i, n, results) = ~(== i n) {{
  true: results  // All patterns processed
  false:
    // Get current pattern
    let pattern = (get patterns i)
    
    // Match based on pattern type
    let result = ~pattern.type {{
      "literal":
        // Use simple string search for literals
        ~(@contains(traffic.text, pattern.text)) {{
          true: {{pattern_id: pattern.id, position: 0}}  // Found
          false: #NoMatch  // Not found
        }}
      "regex":
        // Use regex matcher for regex patterns
        let ast = @parse_regex(pattern.text)
        let nfa = @ast_to_nfa(ast, pattern.id)
        @match_combined_nfa(nfa, traffic.text, 0)
      _: #NoMatch  // Unsupported pattern type
    }}
    
    // Add to results if matched
    let new_results = ~result {{
      #NoMatch: results  // No match
      _: (+ results [result])  // Add to results
    }}
    
    // Continue with next pattern
    @match_sequential_iter(patterns, traffic, (+ i 1), n, new_results)
}}

// Run benchmark
@sequential_benchmark =
  // Get subset of patterns
  let patterns = {pattern_subset}
  
  // Get test traffic - concatenate all samples for thorough testing
  let all_traffic = {{
    id: 0,
    text: (+ (+ (+ (+ @traffic_samples[0].text @traffic_samples[1].text) 
                    @traffic_samples[2].text) @traffic_samples[3].text)
              @traffic_samples[4].text)
  }}
  
  // Run the benchmark
  let start_time = @current_time_ms()
  
  // Match all patterns sequentially
  let matches = @match_sequential(patterns, all_traffic)
  
  let end_time = @current_time_ms()
  let elapsed = (- end_time start_time)
  
  // Return timing and match count
  {{
    elapsed_ms: elapsed,
    match_count: (len matches),
    pattern_count: (len patterns)
  }}

// Use stub for time function
@current_time_ms = 0  // Will be replaced with proper implementation

@main = @sequential_benchmark
"""
    
    # Write to file
    with open("sequential_benchmark.hvml", "w") as f:
        f.write(benchmark_code)
    
    return "sequential_benchmark.hvml"

def create_parallel_benchmark(patterns, traffic, pattern_count):
    """Create a benchmark file that runs patterns in parallel"""
    
    # Limit patterns to the requested count
    pattern_subset = f"(slice @snort_patterns 0 {pattern_count})"
    
    benchmark_code = f"""// Parallel pattern matching benchmark
@include "multi_pattern_impl.hvml"

// Run benchmark
@parallel_benchmark =
  // Get subset of patterns
  let patterns = {pattern_subset}
  
  // Get test traffic - concatenate all samples for thorough testing
  let all_traffic = {{
    id: 0,
    text: (+ (+ (+ (+ @traffic_samples[0].text @traffic_samples[1].text) 
                    @traffic_samples[2].text) @traffic_samples[3].text)
              @traffic_samples[4].text)
  }}
  
  // Build the multi-pattern matcher
  let matcher = @build_snort_matcher(patterns)
  
  // Run the benchmark
  let start_time = @current_time_ms()
  
  // Match all patterns in parallel
  let match_result = @match_traffic(matcher, all_traffic)
  
  let end_time = @current_time_ms()
  let elapsed = (- end_time start_time)
  
  // Return timing and match count
  {{
    elapsed_ms: elapsed,
    match_count: (len match_result.matches),
    pattern_count: (len patterns)
  }}

// Use stub for time function
@current_time_ms = 0  // Will be replaced with proper implementation

@main = @parallel_benchmark
"""
    
    # Write to file
    with open("parallel_benchmark.hvml", "w") as f:
        f.write(benchmark_code)
    
    return "parallel_benchmark.hvml"

def run_benchmark(benchmark_file, hvm_path):
    """Run a benchmark with warmup and multiple iterations, returning averaged results"""
    
    results = []
    
    try:
        # Warmup phase
        print(f"\n  Warming up for {WARMUP_TIME}s...", end="", flush=True)
        warmup_start = time.time()
        warmup_iterations = 0
        
        # Run iterations until warmup time is reached
        while time.time() - warmup_start < WARMUP_TIME:
            subprocess.run([hvm_path, benchmark_file], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         universal_newlines=True,
                         timeout=TIMEOUT)
            warmup_iterations += 1
        
        print(f" done ({warmup_iterations} iterations)")
        
        # Benchmark phase - run multiple iterations
        print(f"  Running {ITERATIONS} iterations...", end="", flush=True)
        
        for i in range(ITERATIONS):
            # Run the benchmark
            iter_start = time.time()
            result = subprocess.run([hvm_path, benchmark_file], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True,
                                   timeout=TIMEOUT)
            iter_end = time.time()
            
            # Calculate elapsed time for this iteration
            elapsed_ms = int((iter_end - iter_start) * 1000)
            
            # Store result
            results.append({
                "elapsed_ms": elapsed_ms,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
            
            # Progress indicator
            print(".", end="", flush=True)
        
        print(" done")
        
        # Calculate statistics
        times = [r["elapsed_ms"] for r in results]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        # Return averaged results
        return {
            "elapsed_ms": avg_time,
            "min_ms": min_time,
            "max_ms": max_time,
            "iterations": ITERATIONS,
            "warmup_iterations": warmup_iterations
        }
            
    except subprocess.TimeoutExpired:
        print(f" benchmark timed out after {TIMEOUT} seconds")
        return {
            "elapsed_ms": TIMEOUT * 1000,
            "min_ms": TIMEOUT * 1000,
            "max_ms": TIMEOUT * 1000,
            "timeout": True
        }
    except Exception as e:
        print(f" error: {e}")
        return {
            "elapsed_ms": 0,
            "min_ms": 0,
            "max_ms": 0,
            "error": str(e)
        }

def run_all_benchmarks(hvm_path):
    """Run all benchmarks and report results"""
    
    # Print header
    print("\nSnort Pattern Matcher Benchmark")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"HVM: {hvm_path}")
    print(f"Configuration: {WARMUP_TIME}s warmup, {ITERATIONS} iterations")
    print("-" * 100)
    
    print(f"{'Pattern Count':<10} | {'Sequential (ms)':<20} | {'Parallel (ms)':<20} | {'Speedup':<10} | {'Notes'}")
    print(f"{'':10} | {'Avg (Min-Max)':<20} | {'Avg (Min-Max)':<20} | {'':<10} | ")
    print("-" * 100)
    
    results = []
    
    # Run benchmarks for different pattern counts
    for count in PATTERN_COUNTS:
        # Create benchmark files
        sequential_file = create_sequential_benchmark("@snort_patterns", "@traffic_samples", count)
        parallel_file = create_parallel_benchmark("@snort_patterns", "@traffic_samples", count)
        
        # Run sequential benchmark
        print(f"\nRunning benchmark with {count} patterns:")
        print(f"- Sequential matching:", flush=True)
        sequential_result = run_benchmark(sequential_file, hvm_path)
        
        # Run parallel benchmark
        print(f"- Parallel matching:", flush=True)
        parallel_result = run_benchmark(parallel_file, hvm_path)
        
        # Calculate speedup
        if sequential_result["elapsed_ms"] > 0 and parallel_result["elapsed_ms"] > 0:
            speedup = sequential_result["elapsed_ms"] / parallel_result["elapsed_ms"]
        else:
            speedup = 0
        
        # Store results for this pattern count
        result = {
            "count": count,
            "sequential": sequential_result,
            "parallel": parallel_result,
            "speedup": speedup
        }
        results.append(result)
        
        # Format result strings
        seq_time = f"{sequential_result['elapsed_ms']:.1f} ({sequential_result['min_ms']:.1f}-{sequential_result['max_ms']:.1f})"
        par_time = f"{parallel_result['elapsed_ms']:.1f} ({parallel_result['min_ms']:.1f}-{parallel_result['max_ms']:.1f})"
        
        # Notes about result (any warnings, timeout, etc.)
        notes = ""
        if "timeout" in sequential_result or "timeout" in parallel_result:
            notes = "Timeout occurred"
        elif "error" in sequential_result or "error" in parallel_result:
            notes = "Error occurred"
            
        # Print results for this pattern count
        print(f"{count:<10} | {seq_time:<20} | {par_time:<20} | {speedup:.2f}x     | {notes}")
    
    # Print summary
    print("\nSummary:")
    print("-" * 100)
    
    # Calculate average speedup across all tests
    if results:
        avg_speedup = sum(r["speedup"] for r in results) / len(results)
        max_speedup = max(r["speedup"] for r in results)
        max_speedup_count = next(r["count"] for r in results if r["speedup"] == max_speedup)
        
        print(f"Average speedup: {avg_speedup:.2f}x")
        print(f"Maximum speedup: {max_speedup:.2f}x (with {max_speedup_count} patterns)")
        
        # Check if speedup increases with pattern count
        first_speedup = results[0]["speedup"]
        last_speedup = results[-1]["speedup"]
        if last_speedup > first_speedup:
            scaling = (last_speedup - first_speedup) / (results[-1]["count"] - results[0]["count"])
            print(f"Speedup scaling: +{scaling:.4f}x per pattern")
            print("Speedup increases with pattern count, suggesting efficient parallelism")
        else:
            print("Speedup does not increase with pattern count")
    
    print("-" * 100)
    print("Note: Higher speedup values indicate better performance of the parallel implementation.")
    print("      Proper multi-core HVM support should significantly improve these results.")

if __name__ == "__main__":
    # Use specified HVM path or default
    hvm_path = sys.argv[1] if len(sys.argv) > 1 else HVM_PATH
    run_all_benchmarks(hvm_path)