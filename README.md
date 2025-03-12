# HVM-Regex: Experimental Regular Expression Engine for HVM3

**IMPORTANT: This is an experimental, proof-of-concept implementation with significant limitations. It was developed with assistance from Claude AI and should not be considered production-ready.**

A pure HVM3 implementation of a regular expression engine designed to explore the characteristics of Higher-order Virtual Machine (HVM3). This implementation attempts to leverage HVM3's parallelism, lazy evaluation, and optimal sharing for pattern matching, though with mixed results.

## Project Status

This project represents an **initial exploration** into implementing regex capabilities in HVM3. Our benchmarking indicates that:

1. **Performance Gap**: The current implementation is approximately 3000-4900x slower than native implementations like Python's `re` module. This is primarily due to HVM3 being an interpreted language without dedicated regex optimizations.

2. **Theoretical Interest**: While not competitive for practical use, the implementation demonstrates interesting applications of HVM3's evaluation model for pattern matching.

3. **Limitations Identified**: Our experimentation revealed several obstacles to efficient regex implementation in pure HVM3, including the lack of optimized string operations and limited compilation optimizations.

4. **Future Potential**: A hybrid approach combining HVM3's parallelism with native implementations for critical operations might yield better results in future work.

## Overview

This experimental engine was designed with the following goals:

1. **HVM3 Compatibility**: Explores HVM3's pattern matching, recursion, and variable handling characteristics.
2. **Parallelism Exploration**: Investigates potential benefits of HVM3's natural parallelism for pattern matching.
3. **Clean Implementation**: Attempts to follow HVM3 idioms for maintainable, understandable code.
4. **Learning Exercise**: Serves as a case study for understanding HVM3's strengths and limitations.

## Features Attempted

The HVM3 regex engine attempts to support:

- Literal string matching
- Character and character class matching
- Alternation (`|`) with parallel evaluation
- Concatenation (sequencing)
- Repetition operators (`*`, `+`, `?`, `{n,m}`) with lazy evaluation
- Anchors (`^`, `$`)
- Word boundaries (`\b`, `\B`)
- Capturing groups and backreferences
- Nested groups (`((a)(b))`)
- Zero-width assertions (lookahead, lookbehind)

Many of these features work correctly for simple cases but may fail for complex patterns or have performance issues.

## Implementation Highlights

### Pattern Representation

Patterns are represented as algebraic data types with constructors for each pattern type:

```hvm
data Pattern {
  #Literal { str }                  // Literal string, e.g., "GET"
  #Char { c }                       // Single character, e.g., 'a'
  #Any                              // Any character (like . in regex)
  #Concat { a b }                   // Concatenation of two patterns
  #Alt { a b }                      // Alternative patterns (a|b)
  #Star { node }                    // Zero or more repetitions (a*)
  #Plus { node }                    // One or more repetitions (a+)
  #Optional { node }                // Zero or one repetition (a?)
  #Repeat { node n }                // Exactly n repetitions (a{n})
  #RepeatRange { node min max }     // Range of repetitions (a{min,max})
  #CharClass { chars }              // Character class (e.g., [abc])
  #NegCharClass { chars }           // Negated character class (e.g., [^abc])
  #Group { node }                   // Capturing group (e.g., (a))
  #AnchorStart                      // Start of string anchor (^)
  #AnchorEnd                        // End of string anchor ($)
  #WordBoundary                     // Word boundary (\b)
  #NonWordBoundary                  // Non-word boundary (\B)
  #PosLookahead { node }            // Positive lookahead (e.g., a(?=b))
  #NegLookahead { node }            // Negative lookahead (e.g., a(?!b))
  #PosLookbehind { node }           // Positive lookbehind (e.g., (?<=a)b)
  #NegLookbehind { node }           // Negative lookbehind (e.g., (?<!a)b)
}
```

## HVM3 Optimization Attempts

The implementation attempts several HVM3-specific optimizations:

1. **Parallel Alternative Matching**: Attempts to evaluate both sides of an alternative pattern (`a|b`) simultaneously
2. **Lazy Evaluation for Repetitions**: Tries to leverage HVM3's natural laziness for repetition operators
3. **Dynamic Character Classes**: Uses a flexible approach to character class matching
4. **Zero-Width Assertions**: Implements lookahead/lookbehind and boundary conditions
5. **Graph Reduction**: Pattern matching expressed to take advantage of HVM3's graph reduction

## Benchmarking Issues

Our benchmarking methodology may have limitations:
- The comparison against optimized native implementations like Python's `re` module may not be entirely fair
- Benchmark design might not fully reflect real-world usage patterns
- Small differences in feature implementations make direct comparisons difficult
- The HVM3 interpreter overhead significantly impacts performance measurements

## Conclusions

This project demonstrates that while HVM3 has interesting characteristics for pattern matching, a pure HVM3 implementation of regex is not currently competitive with native implementations for practical use. The primary limiting factors are:

1. Interpretation overhead
2. Lack of specialized string operations
3. Limited optimization for recursive pattern matching
4. Memory usage patterns

A more promising approach might be a hybrid implementation that uses HVM3 for high-level control flow and parallel pattern evaluation while delegating string operations to native code.

## Getting Started

### Prerequisites

- HVM3 installed and configured
- Python 3.6+ for running benchmarks and tests

### Building and Running

See the documentation in `docs/` for detailed build and usage instructions.

## Documentation

- `docs/IMPLEMENTATION.md` - Details on the implementation approach
- `docs/OPTIMIZATION.md` - Optimization strategies specific to HVM3
- `docs/BENCHMARKS.md` - Performance comparisons and analysis

## Contributors

This project was developed as an exploratory exercise with assistance from Claude AI.

## License

[MIT License](LICENSE)