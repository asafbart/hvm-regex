#!/usr/bin/env python3
"""
Benchmark comparing original multi-pattern matcher implementation with optimized version.
"""

import os
import subprocess
import time
import sys
from datetime import datetime
import platform

# Path to HVM executable
HVM_PATH = "/Users/asafbartov/claudeprojects/hvmsnort/HVM3/dist-newstyle/build/x86_64-osx/ghc-9.12.1/HVM3-0.1.0.0/x/hvml/opt/build/hvml/hvml"

# Number of patterns to test with
PATTERN_COUNTS = [10, 25, 50, 100]

# Benchmark configuration
WARMUP_TIME = 2.0       # Warmup time in seconds
ITERATIONS = 5          # Number of iterations for each test after warmup
TIMEOUT = 300           # Timeout in seconds for each benchmark run

def create_original_benchmark(pattern_count):
    """Create a benchmark file for the original multi-pattern implementation"""
    
    benchmark_code = f"""// Benchmark for original multi-pattern implementation
@include "multi_pattern_impl.hvml"
@include "extended_snort_patterns.hvml"

// Helper function to get current time
@current_time_ms = 0  // Will be replaced with real implementation

// Run benchmark
@benchmark_original =
  // Get patterns to test with
  let patterns = @get_pattern_subset({pattern_count})
  
  // Get test traffic - concatenate all samples for thorough testing
  let all_traffic = {{
    id: 0,
    text: (+ (+ (+ (+ @traffic_samples[0].text @traffic_samples[1].text) 
                  @traffic_samples[2].text) @traffic_samples[3].text)
            @traffic_samples[4].text)
  }}
  
  // Build the multi-pattern matcher (preprocessing)
  let matcher = @build_extended_matcher(patterns)
  
  // Start timing
  let start_time = @current_time_ms()
  
  // Match input against patterns
  let match_result = @match_traffic(matcher, all_traffic)
  
  // End timing
  let end_time = @current_time_ms()
  let elapsed = (- end_time start_time)
  
  // Return timing and match details
  {{
    elapsed_ms: elapsed,
    match_count: (len match_result.matches),
    pattern_count: (len patterns)
  }}

@main = @benchmark_original
"""
    
    # Write to file
    with open("original_benchmark.hvml", "w") as f:
        f.write(benchmark_code)
    
    return "original_benchmark.hvml"

def create_optimized_benchmark(pattern_count):
    """Create a benchmark file for the optimized multi-pattern implementation"""
    
    benchmark_code = f"""// Benchmark for optimized multi-pattern implementation
@include "optimized_multi_pattern.hvml"
@include "extended_snort_patterns.hvml"

// Helper function to get current time
@current_time_ms = 0  // Will be replaced with real implementation

// Function to match patterns from extended_snort_patterns.hvml with the optimized implementation
@match_optimized(patterns, traffic) =
  // Group patterns by type
  let grouped = @group_patterns_by_type(patterns)
  
  // Build specialized matchers
  let literals_matcher = @build_ac_automaton(grouped.literals)
  let regex_matcher = @combine_nfas_optimized(@map(grouped.regexes, @pattern_to_nfa_optimized))
  
  // Create matcher
  let matcher = {{
    literals: literals_matcher,
    regexes: regex_matcher
  }}
  
  // Match using optimized algorithm
  let literal_results = @match_ac_optimized(matcher.literals, traffic.text)
  let regex_results = @match_combined_nfa_optimized(matcher.regexes, traffic.text)
  
  // Combine results
  let all_results = @combine_results_fast([literal_results, regex_results])
  
  // Return traffic ID with matches
  {{
    traffic_id: traffic.id,
    matches: all_results
  }}

// Run benchmark
@benchmark_optimized =
  // Get patterns to test with
  let patterns = @get_pattern_subset({pattern_count})
  
  // Get test traffic - concatenate all samples for thorough testing
  let all_traffic = {{
    id: 0,
    text: (+ (+ (+ (+ @traffic_samples[0].text @traffic_samples[1].text) 
                  @traffic_samples[2].text) @traffic_samples[3].text)
            @traffic_samples[4].text)
  }}
  
  // Start timing
  let start_time = @current_time_ms()
  
  // Match input against patterns
  let match_result = @match_optimized(patterns, all_traffic)
  
  // End timing
  let end_time = @current_time_ms()
  let elapsed = (- end_time start_time)
  
  // Return timing and match details
  {{
    elapsed_ms: elapsed,
    match_count: (len match_result.matches),
    pattern_count: (len patterns)
  }}

@main = @benchmark_optimized
"""
    
    # Write to file
    with open("optimized_benchmark.hvml", "w") as f:
        f.write(benchmark_code)
    
    return "optimized_benchmark.hvml"

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

def run_comparative_benchmarks(hvm_path):
    """Run benchmarks for both original and optimized implementations"""
    
    # Print header
    print("\nMulti-Pattern Matcher Optimization Benchmark")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"HVM: {hvm_path}")
    print("-" * 100)
    
    print(f"{'Pattern Count':<10} | {'Original (ms)':<20} | {'Optimized (ms)':<20} | {'Speedup':<10} | {'Notes'}")
    print(f"{'':10} | {'Avg (Min-Max)':<20} | {'Avg (Min-Max)':<20} | {'':<10} | ")
    print("-" * 100)
    
    results = []
    
    # Run benchmarks for different pattern counts
    for count in PATTERN_COUNTS:
        # Create benchmark files
        original_file = create_original_benchmark(count)
        optimized_file = create_optimized_benchmark(count)
        
        # Run original benchmark
        print(f"\nBenchmarking with {count} patterns:")
        print(f"- Original implementation:", flush=True)
        original_result = run_benchmark(original_file, hvm_path)
        
        # Run optimized benchmark
        print(f"- Optimized implementation:", flush=True)
        optimized_result = run_benchmark(optimized_file, hvm_path)
        
        # Calculate speedup
        if original_result["elapsed_ms"] > 0 and optimized_result["elapsed_ms"] > 0:
            speedup = original_result["elapsed_ms"] / optimized_result["elapsed_ms"]
        else:
            speedup = 0
        
        # Store results for this pattern count
        result = {
            "count": count,
            "original": original_result,
            "optimized": optimized_result,
            "speedup": speedup
        }
        results.append(result)
        
        # Format result strings
        orig_time = f"{original_result['elapsed_ms']:.1f} ({original_result['min_ms']:.1f}-{original_result['max_ms']:.1f})"
        opt_time = f"{optimized_result['elapsed_ms']:.1f} ({optimized_result['min_ms']:.1f}-{optimized_result['max_ms']:.1f})"
        
        # Notes about result (any warnings, timeout, etc.)
        notes = ""
        if "timeout" in original_result or "timeout" in optimized_result:
            notes = "Timeout occurred"
        elif "error" in original_result or "error" in optimized_result:
            notes = "Error occurred"
            
        # Print results for this pattern count
        print(f"{count:<10} | {orig_time:<20} | {opt_time:<20} | {speedup:.2f}x     | {notes}")
    
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
            print("Speedup increases with pattern count, showing the optimization benefits")
        else:
            print("Speedup is consistent across pattern counts")
    
    print("-" * 100)
    
    # Save results to file
    save_results_to_file(results)

def save_results_to_file(results):
    """Save benchmark results to a markdown file"""
    
    with open("OPTIMIZATION_BENCHMARK_RESULTS.md", "w") as f:
        f.write("# Multi-Pattern Matcher Optimization Benchmark Results\n\n")
        f.write("## Environment\n")
        f.write(f"- Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"- System: {platform.system()} {platform.release()} ({platform.machine()})\n")
        f.write(f"- HVM: HVM3 build\n")
        f.write(f"- Configuration: {WARMUP_TIME}s warmup, {ITERATIONS} iterations per test\n\n")
        
        f.write("## Results\n\n")
        f.write("| Pattern Count | Original (ms)        | Optimized (ms)       | Speedup | Notes |\n")
        f.write("|---------------|---------------------|---------------------|---------|-------|\n")
        
        for result in results:
            count = result["count"]
            orig = result["original"]
            opt = result["optimized"]
            speedup = result["speedup"]
            
            notes = ""
            if "timeout" in orig or "timeout" in opt:
                notes = "Timeout"
            elif "error" in orig or "error" in opt:
                notes = "Error"
                
            orig_time = f"{orig['elapsed_ms']:.1f} ({orig['min_ms']:.1f}-{orig['max_ms']:.1f})"
            opt_time = f"{opt['elapsed_ms']:.1f} ({opt['min_ms']:.1f}-{opt['max_ms']:.1f})"
            
            f.write(f"| {count:<13} | {orig_time:<19} | {opt_time:<19} | {speedup:.2f}x   | {notes} |\n")
        
        f.write("\n## Analysis\n\n")
        
        if results:
            avg_speedup = sum(r["speedup"] for r in results) / len(results)
            max_speedup = max(r["speedup"] for r in results)
            max_speedup_count = next(r["count"] for r in results if r["speedup"] == max_speedup)
            
            f.write(f"- **Average Speedup**: {avg_speedup:.2f}x\n")
            f.write(f"- **Maximum Speedup**: {max_speedup:.2f}x (with {max_speedup_count} patterns)\n")
            
            # Check if speedup increases with pattern count
            first_speedup = results[0]["speedup"]
            last_speedup = results[-1]["speedup"]
            if last_speedup > first_speedup:
                scaling = (last_speedup - first_speedup) / (results[-1]["count"] - results[0]["count"])
                f.write(f"- **Speedup Scaling**: +{scaling:.4f}x per pattern\n")
                f.write("- **Scaling Behavior**: Speedup increases with pattern count\n")
            else:
                f.write("- **Scaling Behavior**: Speedup is consistent across pattern counts\n")
        
        f.write("\n## Optimization Strategies\n\n")
        f.write("The optimized implementation includes the following improvements:\n\n")
        f.write("1. **Memory Efficiency**:\n")
        f.write("   - Streamlined data structures with smaller memory footprint\n")
        f.write("   - More efficient string handling with fewer allocations\n")
        f.write("   - Batch processing of patterns for better memory locality\n\n")
        
        f.write("2. **Algorithm Optimizations**:\n")
        f.write("   - Single-pass pattern classification\n")
        f.write("   - Optimized Aho-Corasick automaton construction\n")
        f.write("   - More efficient NFA operations with better state representation\n")
        f.write("   - Caching for regex parsing to avoid repeated work\n\n")
        
        f.write("3. **Function Call Reduction**:\n")
        f.write("   - Iterative implementations instead of recursive where possible\n")
        f.write("   - Batch processing to reduce function call overhead\n")
        f.write("   - Early termination for empty inputs and edge cases\n\n")
        
        f.write("4. **Improved Data Locality**:\n")
        f.write("   - Better memory layout for cache efficiency\n")
        f.write("   - Processing patterns in batches to improve cache hits\n")
        f.write("   - Minimizing data structure nesting\n\n")
        
        f.write("## Conclusion\n\n")
        if results and avg_speedup > 1.0:
            f.write(f"The optimized implementation achieves a {avg_speedup:.2f}x average speedup over the original implementation. ")
            if last_speedup > first_speedup:
                f.write("The benefits of optimization increase with larger pattern sets, suggesting that the approach scales better with more patterns. ")
            f.write("These optimizations demonstrate that even within the constraints of the current HVM implementation, significant performance improvements are possible through careful algorithm design and memory management.\n\n")
        else:
            f.write("The optimized implementation shows similar performance to the original implementation. This suggests that further optimizations or different approaches may be needed to achieve significant performance improvements.\n\n")
            
        f.write("Future work should focus on:\n")
        f.write("1. Improved parallelism strategies for multi-core environments\n")
        f.write("2. Further memory optimizations for very large pattern sets\n")
        f.write("3. More specialized algorithms for different pattern types\n")

if __name__ == "__main__":
    # Use specified HVM path or default
    hvm_path = sys.argv[1] if len(sys.argv) > 1 else HVM_PATH
    run_comparative_benchmarks(hvm_path)