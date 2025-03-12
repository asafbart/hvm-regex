# HVM-Regex: Regular Expression Engine for HVM3

A pure HVM3 implementation of a regular expression engine designed specifically for the unique characteristics of Higher-order Virtual Machine (HVM3). This implementation leverages HVM3's parallelism, lazy evaluation, and optimal sharing for efficient pattern matching.

## Overview

This engine is designed with the following goals:

1. **HVM3 Compatibility**: Uses HVM3's pattern matching, recursion, and avoids variable reuse issues.
2. **Performance**: Takes advantage of HVM3's lazy evaluation and natural parallelism for efficient matching.
3. **Clean Implementation**: Follows HVM3 idioms for maintainable, understandable code.
4. **Network Security Focus**: Optimized for patterns commonly found in network traffic inspection.

## Features

The HVM3 regex engine supports:

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

## HVM3 Optimizations

The implementation uses several HVM3-specific optimizations:

1. **Parallel Alternative Matching**: Evaluates both sides of an alternative pattern (`a|b`) simultaneously
2. **Lazy Evaluation for Repetitions**: Leverages HVM3's natural laziness for repetition operators
3. **Dynamic Character Classes**: Uses a flexible approach to character class matching
4. **Zero-Width Assertions**: Efficiently implements lookahead/lookbehind and boundary conditions
5. **Graph Reduction**: Pattern matching expressed to take advantage of HVM3's graph reduction

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

## License

[MIT License](LICENSE)