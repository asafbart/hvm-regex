#!/usr/bin/env python3
"""
Comprehensive benchmark script to compare all regex implementations:
1. Python's built-in re module
2. Original HVM regex implementation (basic_regex.hvml)
3. Optimized HVM3 regex implementation (optimized_regex.hvml)
4. HVM3 regex with parser (regex_parser.hvml)

This provides a full performance comparison across all implementations.
"""

import os
import subprocess
import time
import re
import statistics
import sys
from datetime import datetime
import platform
import json

def create_benchmark_hvml(regex_file, pattern_expr, text, iterations=100):
    """Generate a benchmark HVM file for timing hard-coded regex operations"""
    
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

def create_parser_benchmark_hvml(regex_pattern, text, iterations=100):
    """Generate a benchmark HVM file for timing regex operations with parser"""
    
    benchmark_code = f"""// Automatically generated benchmark file
// Include the regex parser
@include "regex_parser.hvml"

// Benchmark function
@benchmark =
  // Pattern and text
  ! pattern = "{regex_pattern}"
  ! text = "{text}"
  ! iterations = {iterations}
  
  // Run multiple iterations
  @run_iterations(i) =
    ~(== i 0) {{
      1: 0  // Done
      0:
        // Run the match
        ! result = @match_regex(pattern, text, 0)
        
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
    benchmark_file = f"parser_benchmark_{hash(regex_pattern)}.hvml"
    with open(benchmark_file, "w") as f:
        f.write(benchmark_code)
    
    return benchmark_file

def run_hvm_benchmark(hvml_path, regex_file, pattern_expr, text, iterations=100):
    """Run a benchmark for an HVM regex implementation with hard-coded patterns"""
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
            "output": result.stdout,
            "error": result.stderr
        }
    finally:
        # Clean up the benchmark file
        if os.path.exists(benchmark_file):
            os.remove(benchmark_file)

def run_parser_benchmark(hvml_path, regex_pattern, text, iterations=100):
    """Run a benchmark for an HVM regex implementation with parser"""
    benchmark_file = create_parser_benchmark_hvml(regex_pattern, text, iterations)
    
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
            "output": result.stdout,
            "error": result.stderr
        }
    finally:
        # Clean up the benchmark file
        if os.path.exists(benchmark_file):
            os.remove(benchmark_file)

def run_python_re_benchmark(pattern, text, iterations=100):
    """Run a benchmark for Python's built-in re module"""
    try:
        # Compile the pattern first (one-time cost)
        compile_start = time.time()
        compiled_re = re.compile(pattern)
        compile_end = time.time()
        compile_time = compile_end - compile_start
        
        # Measure the time it takes to run the benchmark
        start_time = time.time()
        for _ in range(iterations):
            match = compiled_re.match(text)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        matches_per_second = iterations / elapsed_time
        
        return {
            "elapsed_time": elapsed_time,
            "compile_time": compile_time,
            "matches_per_second": matches_per_second,
            "matched": match is not None
        }
    except re.error as e:
        return {
            "error": str(e),
            "elapsed_time": 0,
            "matches_per_second": 0,
            "matched": False
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
            "name": "Concatenation",
            "pattern": "ab",
            "text": "abcdef",
            "python_re": "ab",
            "basic_pattern": "#Concat2",
            "optimized_pattern": "#Concat{#Char{\"a\"} #Char{\"b\"}}"
        },
        {
            "name": "Alternation",
            "pattern": "a|b",
            "text": "abcdef",
            "python_re": "a|b",
            "basic_pattern": "#Choice1",
            "optimized_pattern": "#Alt{#Char{\"a\"} #Char{\"b\"}}"
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
            "name": "Complex Pattern",
            "pattern": "a(b|c)*d",
            "text": "abcbcd",
            "python_re": "a(b|c)*d",
            "basic_pattern": None,  # Not supported in basic regex
            "optimized_pattern": None  # Need to build this expression
        }
    ]
    
    # Number of iterations for each benchmark
    iterations = 100  # Reduced for HVM which is slower
    python_iterations = 10000  # More for Python to get more accurate results
    
    # Results table header
    headers = ["Benchmark", "Python re", "Basic HVM", "Opt HVM", "Parser HVM", "Python/Basic", "Python/Opt", "Python/Parser"]
    header_line = " | ".join(f"{h:<15}" for h in headers)
    print(header_line)
    print("-" * len(header_line))
    
    # Run each benchmark
    for benchmark in benchmarks:
        name = benchmark["name"]
        pattern = benchmark["pattern"]
        text = benchmark["text"]
        python_re_pattern = benchmark["python_re"]
        basic_pattern = benchmark["basic_pattern"]
        optimized_pattern = benchmark["optimized_pattern"]
        
        # Python re benchmark
        python_result = run_python_re_benchmark(python_re_pattern, text, python_iterations)
        python_speed = format_value(python_result["matches_per_second"])
        
        # Basic HVM regex benchmark
        if basic_pattern:
            basic_result = run_hvm_benchmark(hvml_path, "basic_regex.hvml", basic_pattern, text, iterations)
            basic_speed = format_value(basic_result["matches_per_second"])
            python_basic_ratio = python_result["matches_per_second"] / basic_result["matches_per_second"] if basic_result["matches_per_second"] > 0 else "N/A"
            if isinstance(python_basic_ratio, float):
                python_basic_ratio = f"{python_basic_ratio:.1f}x"
        else:
            basic_speed = "N/A"
            python_basic_ratio = "N/A"
        
        # Optimized HVM regex benchmark
        if optimized_pattern:
            optimized_result = run_hvm_benchmark(hvml_path, "optimized_regex.hvml", optimized_pattern, text, iterations)
            optimized_speed = format_value(optimized_result["matches_per_second"])
            python_opt_ratio = python_result["matches_per_second"] / optimized_result["matches_per_second"] if optimized_result["matches_per_second"] > 0 else "N/A"
            if isinstance(python_opt_ratio, float):
                python_opt_ratio = f"{python_opt_ratio:.1f}x"
        else:
            optimized_speed = "N/A"
            python_opt_ratio = "N/A"
            
        # Parser HVM regex benchmark
        parser_result = run_parser_benchmark(hvml_path, pattern, text, iterations)
        parser_speed = format_value(parser_result["matches_per_second"])
        python_parser_ratio = python_result["matches_per_second"] / parser_result["matches_per_second"] if parser_result["matches_per_second"] > 0 else "N/A"
        if isinstance(python_parser_ratio, float):
            python_parser_ratio = f"{python_parser_ratio:.1f}x"
        
        # Print results
        row = [name, python_speed, basic_speed, optimized_speed, parser_speed, python_basic_ratio, python_opt_ratio, python_parser_ratio]
        row_line = " | ".join(f"{cell:<15}" for cell in row)
        print(row_line)
    
    print("-" * len(header_line))
    print("Note: Higher values for operations/second are better.")
    print("      The ratio columns show how many times faster Python's re module is compared to each HVM implementation.")

if __name__ == "__main__":
    # Use the specified HVM path if provided, otherwise use path to installed hvml
    hvml_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/asafbartov/claudeprojects/hvmsnort/HVM3/dist-newstyle/build/x86_64-osx/ghc-9.12.1/HVM3-0.1.0.0/x/hvml/opt/build/hvml/hvml"
    run_all_benchmarks(hvml_path)