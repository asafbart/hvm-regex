#!/usr/bin/env python3
"""
Benchmark script to compare the performance of different regex implementations:
1. Python's built-in re module
2. Original HVM regex implementation (basic_regex.hvml)
3. Optimized HVM3 regex implementation (optimized_regex.hvml)
"""

import os
import subprocess
import time
import re
import statistics
import sys
from datetime import datetime
import platform

def create_benchmark_hvml(regex_file, pattern_expr, text, iterations=100):
    """Generate a benchmark HVM file for timing regex operations"""
    
    with open(regex_file, "r") as f:
        regex_content = f.read()
    
    benchmark_code = f"""// Benchmark file for {regex_file}
{regex_content}

// Benchmark function
@benchmark =
  // Pattern and text
  ! pattern = {pattern_expr}
  ! text = "{text}"
  ! iterations = {iterations}
  
  // Run multiple iterations
  @run_iterations(i) =
    ~(== i 0) {{
      1: 0  // Done
      0:
        // Run the match
        ! result = @match(pattern, text, 0)
        
        // Continue with next iteration
        @run_iterations((- i 1))
    }}
  
  // Start the benchmark
  @run_iterations(iterations)
  
  // Return success
  1

// Use the benchmark function
@main = @benchmark
"""
    
    # Create a temporary benchmark file
    benchmark_file = f"{os.path.splitext(os.path.basename(regex_file))[0]}_benchmark.hvml"
    with open(benchmark_file, "w") as f:
        f.write(benchmark_code)
    
    return benchmark_file

def run_hvm_benchmark(hvml_path, regex_file, pattern_expr, text, iterations=100):
    """Run a benchmark for an HVM regex implementation"""
    benchmark_file = create_benchmark_hvml(regex_file, pattern_expr, text, iterations)
    
    try:
        # Measure the time it takes to run the benchmark
        start_time = time.time()
        result = subprocess.run(
            [hvml_path, "run", benchmark_file],
            capture_output=True,
            text=True,
            check=False,
        )
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        matches_per_second = iterations / elapsed_time
        
        return {
            "elapsed_time": elapsed_time,
            "matches_per_second": matches_per_second,
            "output": result.stdout
        }
    finally:
        # Clean up the benchmark file
        if os.path.exists(benchmark_file):
            os.remove(benchmark_file)

def run_python_re_benchmark(pattern, text, iterations=100):
    """Run a benchmark for Python's built-in re module"""
    compiled_re = re.compile(pattern)
    
    # Measure the time it takes to run the benchmark
    start_time = time.time()
    for _ in range(iterations):
        match = compiled_re.match(text)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    matches_per_second = iterations / elapsed_time
    
    return {
        "elapsed_time": elapsed_time,
        "matches_per_second": matches_per_second
    }

def format_value(value):
    """Format a number for display"""
    if value >= 1000000:
        return f"{value/1000000:.2f}M"
    elif value >= 1000:
        return f"{value/1000:.2f}K"
    else:
        return f"{value:.2f}"

def run_all_benchmarks(hvml_path="hvml"):
    """Run all benchmarks and display results"""
    # System information
    print(f"Benchmark run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python: {platform.python_version()}")
    print(f"HVM: {hvml_path}")
    print("-" * 80)
    
    # Benchmark configurations
    benchmarks = [
        {
            "name": "Literal Match",
            "pattern": "GET",
            "text": "GET /index.html HTTP/1.1",
            "python_re": "GET",
            "basic_pattern": "#Literal",
            "optimized_pattern": "#Literal{\"GET\"}"
        },
        {
            "name": "Simple Concatenation",
            "pattern": "ab",
            "text": "abcdef",
            "python_re": "ab",
            "basic_pattern": "#Concat2",
            "optimized_pattern": "#Concat{#Char{\"a\"} #Char{\"b\"}}"
        },
        {
            "name": "Alternation (first)",
            "pattern": "a|b",
            "text": "abcdef",
            "python_re": "a|b",
            "basic_pattern": "#Choice1",
            "optimized_pattern": "#Alt{#Char{\"a\"} #Char{\"b\"}}"
        },
        {
            "name": "Alternation (second)",
            "pattern": "x|b",
            "text": "bcd",
            "python_re": "x|b",
            "basic_pattern": "#Choice2",
            "optimized_pattern": "#Alt{#Char{\"x\"} #Char{\"b\"}}"
        },
        {
            "name": "Star Repetition",
            "pattern": "a*",
            "text": "aaabcd",
            "python_re": "a*",
            "basic_pattern": "#Star",
            "optimized_pattern": "#Star{#Char{\"a\"}}"
        },
        {
            "name": "Plus Repetition",
            "pattern": "a+",
            "text": "aaabcd",
            "python_re": "a+",
            "basic_pattern": "#Plus",
            "optimized_pattern": "#Plus{#Char{\"a\"}}"
        },
        {
            "name": "Character Class",
            "pattern": "[abc]",
            "text": "abcdef",
            "python_re": "[abc]",
            "basic_pattern": "#CharClass1",
            "optimized_pattern": "#CharClass{\"abc\"}"
        },
        {
            "name": "Capturing Group",
            "pattern": "(a)",
            "text": "abcdef",
            "python_re": "(a)",
            "basic_pattern": "#Group1",
            "optimized_pattern": "#Group{#Char{\"a\"}}"
        },
        {
            "name": "Positive Lookahead",
            "pattern": "a(?=b)",
            "text": "abcdef",
            "python_re": "a(?=b)",
            "basic_pattern": "#PosLookaheadA",
            "optimized_pattern": "#Concat{#Char{\"a\"} #PosLookahead{#Char{\"b\"}}}"
        }
    ]
    
    # Number of iterations for each benchmark
    iterations = 1000
    
    # Results table header
    print(f"{'Benchmark':<25} {'Python re (ops/s)':<20} {'Basic HVM (ops/s)':<20} {'Optimized HVM (ops/s)':<20} {'Opt/Basic Ratio':<15}")
    print("-" * 100)
    
    # Run each benchmark
    for benchmark in benchmarks:
        # Python re benchmark
        python_result = run_python_re_benchmark(benchmark["python_re"], benchmark["text"], iterations)
        
        # Basic HVM regex benchmark
        basic_result = run_hvm_benchmark(hvml_path, "basic_regex.hvml", benchmark["basic_pattern"], benchmark["text"], iterations)
        
        # Optimized HVM regex benchmark
        optimized_result = run_hvm_benchmark(hvml_path, "optimized_regex.hvml", benchmark["optimized_pattern"], benchmark["text"], iterations)
        
        # Calculate ratio of optimized vs basic
        if basic_result["matches_per_second"] > 0:
            ratio = optimized_result["matches_per_second"] / basic_result["matches_per_second"]
        else:
            ratio = float('inf')
        
        # Print results
        print(f"{benchmark['name']:<25} {format_value(python_result['matches_per_second']):<20} {format_value(basic_result['matches_per_second']):<20} {format_value(optimized_result['matches_per_second']):<20} {ratio:.2f}x")
    
    print("-" * 100)
    print("Note: Higher values for operations/second (ops/s) are better.")
    print("      The Opt/Basic Ratio shows how many times faster the optimized version is compared to the basic version.")

if __name__ == "__main__":
    # Use the specified HVM path if provided, otherwise use "hvml"
    hvml_path = sys.argv[1] if len(sys.argv) > 1 else "hvml"
    run_all_benchmarks(hvml_path)