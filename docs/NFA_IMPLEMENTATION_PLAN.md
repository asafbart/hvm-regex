# NFA-Based Regex Implementation Plan

## Background

Our current attempt to implement Thompson's algorithm with NFA simulation in `regex_nfa_fixed.hvml` encountered parser errors with HVM. This document outlines a plan to fix and improve this implementation, which should offer significant performance benefits over our backtracking approaches.

## Why Thompson's NFA/DFA Approach?

1. **Guaranteed linear time complexity** - Unlike backtracking approaches which can have exponential worst-case behavior
2. **More predictable performance** - Performance depends linearly on input length, not pattern complexity
3. **Better suited for security applications** - Resistant to ReDoS (Regular Expression Denial of Service) attacks
4. **Potential for parallelism** - Multiple states can be processed in parallel, fitting HVM's execution model

## Implementation Plan

### Step 1: Fix Parser Errors

1. **Simplify initial implementation**
   - Break complex file into smaller modules
   - Avoid nested pattern matching that might confuse HVM parser
   - Start with minimal functionality to get a working base

2. **Use simpler data structures**
   - Replace linked lists with arrays where appropriate
   - Avoid deeply nested data structures
   - Use simpler tuple representations

3. **Test incrementally**
   - Build smallest possible subset that parses correctly
   - Add functionality one feature at a time
   - Ensure each addition passes parser checks

### Step 2: Core NFA Engine

1. **Implement core NFA construction**
   - Build Thompson construction for basic patterns (literals, concatenation, alternation)
   - Implement epsilon closure computation
   - Create state transition functions

2. **Add subset construction for DFA**
   - Implement powerset construction algorithm
   - Build DFA transition table
   - Optimize state representation

3. **Create matcher using DFA**
   - Implement efficient state transition logic
   - Add support for capturing groups (challenging with pure NFA/DFA)
   - Implement anchors and boundaries

### Step 3: Performance Optimizations

1. **Specialized character class representation**
   - Use bitmap for ASCII character classes
   - Implement range-based representation for efficiency
   - Add specialized fast paths for common classes (digits, alphanumeric, etc.)

2. **State set optimization**
   - Use more efficient state set representation
   - Implement bit vector for small state sets
   - Pool common state sets

3. **Pattern-specific optimizations**
   - Add fast paths for common patterns
   - Pre-compute transitions for frequent subpatterns
   - Implement specialized matchers for common regex idioms

### Step 4: Advanced Features

1. **Implement capturing groups**
   - Add tagging to NFA states
   - Track tag values during simulation
   - Reconstruct captures from tags

2. **Add advanced assertions**
   - Implement lookahead and lookbehind
   - Add word boundaries and anchors
   - Support backreferences (challenging with pure NFA/DFA)

3. **Implement lazy quantifiers**
   - Add support for non-greedy repetition
   - Implement possessive quantifiers
   - Add atomic grouping

## Implementation Strategy

Break down the implementation into small, testable modules:

1. **NFA core** - Basic state and transition representation
2. **Pattern compiler** - Convert regex AST to NFA
3. **Epsilon closure** - Compute epsilon closure of states
4. **DFA construction** - Convert NFA to DFA using subset construction
5. **Matcher** - Match DFA against input text
6. **Captures** - Track and extract capturing groups

Each module should have simple test cases and be developed incrementally.

## HVM-Specific Considerations

1. **Embrace parallelism**
   - Structure NFA simulation to benefit from HVM's parallel reduction
   - Use HVM's concurrency model for simultaneous state transitions
   - Leverage implicit parallelism in alternation matching

2. **Optimize for HVM runtime**
   - Use HVM's primitives efficiently
   - Structure code to benefit from HVM's evaluation model
   - Minimize allocations and copying

3. **Work within HVM constraints**
   - Avoid complex nested pattern matching
   - Structure code to work with HVM's parser limitations
   - Stay within HVM's type system capabilities

## Expected Challenges

1. **Parser limitations**
   - HVM parser has some limitations with complex pattern matching
   - Recursive implementations may be challenging

2. **Capturing groups**
   - Pure Thompson NFA/DFA approach doesn't naturally support captures
   - Need to extend with tagging mechanism

3. **Complex assertions**
   - Lookaround assertions are challenging with pure NFA/DFA
   - Backreferences cannot be represented in regular languages

## Success Criteria

1. **Correctness** - Correctly match patterns according to expected semantics
2. **Performance** - At least 3-5x improvement over backtracking implementation
3. **Scalability** - Handle complex patterns without exponential slowdown
4. **Maintainability** - Clean, modular code that can be extended

## Next Steps

1. Start with a minimal NFA implementation that passes HVM's parser
2. Implement basic Thompson construction for simple patterns
3. Build epsilon closure and NFA simulation
4. Add subset construction for DFA conversion
5. Extend with capturing groups and assertions

By following this plan, we aim to develop a robust NFA/DFA-based regex engine in pure HVM that delivers significantly better performance and predictability than our current implementations.