# Regex Performance Testing Framework

This document outlines the performance testing framework for our HVM3-compatible regex implementation.

## Performance Metrics

We'll measure the following performance aspects:

1. **Compilation Time**: Time taken to parse and compile regex patterns
2. **Matching Time**: Time taken to match patterns against input strings
3. **Memory Usage**: Memory consumed during pattern compilation and matching
4. **Scaling Behavior**: How performance scales with input size and pattern complexity

## Test Categories

### 1. Pattern Complexity Tests

Test how performance scales with pattern complexity:

| Pattern Type | Example | Complexity |
|--------------|---------|------------|
| Simple       | `^abc$` | Low        |
| Medium       | `^a+b*[0-9]{1,3}$` | Medium |
| Complex      | `^(a+\|b+)[0-9]+(\.[0-9]+)?[a-z]*$` | High |
| Very Complex | `^(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$` | Very High |

### 2. Input Size Tests

Test how performance scales with input size:

| Input Size | Characters | Example |
|------------|------------|---------|
| Tiny       | < 10       | "abcdef" |
| Small      | 10-100     | Short paragraph |
| Medium     | 100-1,000  | Multiple paragraphs |
| Large      | 1K-10K     | Small document |
| Very Large | 10K-100K   | Large document |
| Huge       | > 100K     | Very large document |

### 3. Feature-specific Tests

Measure the performance impact of specific regex features:

- Alternation (`a|b|c`)
- Repetition (`a*`, `b+`, `c?`)
- Character classes (`[a-z]`, `[^0-9]`)
- Backreferences (`(a+)b\1`)
- Lookahead/lookbehind (`a(?=b)`, `(?<=a)b`)
- Unicode character classes (`\p{L}`, `\p{N}`)

### 4. Pathological Cases

Test performance on regex patterns known to cause exponential backtracking:

- Nested repetition: `(a+)+b`
- Overlapping alternatives: `(a|a)+b`
- Greedy vs lazy repetition: `.*a.*` vs `.*?a.*?`

## Benchmarking Methodology

1. **Warm-up Runs**: Execute the test several times to warm up the system
2. **Multiple Iterations**: Run each test multiple times (typically 5-10)
3. **Statistical Analysis**: Report median, mean, and standard deviation
4. **System Isolation**: Minimize interference from other processes
5. **Comparison Baseline**: Compare against other regex implementations (PCRE, RE2)

## Implementation

The benchmarking framework will consist of:

1. **Benchmark Runner**: Executes the tests and collects data
2. **Pattern Generator**: Generates test patterns of varying complexity
3. **Input Generator**: Generates test inputs of varying sizes
4. **Results Analyzer**: Processes and reports benchmark results
5. **Visualization Tools**: Creates charts and graphs to visualize performance data

## Optimization Targets

Based on benchmark results, we'll focus optimizations on:

1. Compilation performance for complex patterns
2. Matching performance for large inputs
3. Memory usage patterns
4. Reducing backtracking overhead
5. Parallel matching opportunities

## Reporting

Performance reports will include:

1. Compilation time for each pattern category
2. Matching time for each input size and pattern category
3. Memory usage statistics
4. Scaling behavior charts
5. Comparison with baseline implementations
6. Identification of performance bottlenecks
7. Recommendations for optimization

## Usage Instructions

To run the benchmarks:

```bash
./run_benchmarks.sh --type all
./run_benchmarks.sh --type pattern-complexity
./run_benchmarks.sh --type input-size
./run_benchmarks.sh --type features
./run_benchmarks.sh --type pathological
```

Output will be saved to the `benchmarks/results` directory in both raw data and chart formats.