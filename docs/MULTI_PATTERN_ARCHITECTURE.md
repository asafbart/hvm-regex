# Multi-Pattern Matching Architecture for HVM

This document describes a specialized architecture for efficiently matching hundreds or thousands of regular expression patterns simultaneously using HVM's natural parallelism.

## Key Insight

HVM's parallel evaluation model is not optimal for optimizing a single regex pattern but provides unique advantages for matching many patterns simultaneously. By designing a system that leverages this parallelism at multiple levels, we can create a highly efficient multi-pattern matcher for applications like network intrusion detection systems (Snort, Suricata).

## Architecture Overview

The multi-pattern matcher consists of several specialized components working together:

```
Input Stream 
    ↓
Pattern Classification & Grouping
    ↓
┌───────────────────────────────────────┐
│ Specialized Parallel Matchers         │
├───────────┬───────────┬───────────────┤
│ Literal   │ Prefix    │ Regex State   │
│ Matcher   │ Matcher   │ Machine       │
│ (Aho-     │ (Common   │ (Combined     │
│ Corasick) │ Prefixes) │ NFA/Automaton)│
└───────────┴───────────┴───────────────┘
    ↓
Result Aggregation & Reporting
```

## Key Components

### 1. Pattern Classification

Patterns are analyzed and classified into groups that can be handled by specialized matchers:

- **Literal Patterns**: Fixed strings like "GET /admin" or "UNION SELECT"
- **Prefix Patterns**: Patterns sharing common prefixes
- **Character Class Patterns**: Patterns primarily using character classes ([a-z], [0-9], etc.)
- **General Regex Patterns**: Complex patterns needing full regex machinery

This classification is performed during initialization, not during matching.

### 2. Aho-Corasick Automaton for Literals

For literal strings (a common case in intrusion detection), an Aho-Corasick automaton provides O(n) matching time regardless of the number of patterns:

- Single pass through the input text
- Natural fit for HVM's parallel state tracking
- Reports all matches at once
- No backtracking required

### 3. Prefix-based Matching

For patterns sharing common prefixes:

- Group patterns by prefix
- Match the prefix first as a fast path
- Only evaluate the rest of the pattern if the prefix matches
- HVM can evaluate all prefix groups in parallel

### 4. Combined NFA for Regex Patterns

For general regex patterns:

- Compile each pattern to an NFA
- Combine all NFAs with epsilon transitions from a single start state
- Track all active states simultaneously using HVM's parallel execution
- Use bit vectors to represent active states for efficient operations

### 5. Bit-Parallel Operations

For character class processing:

- Represent character classes as bit vectors
- Use bit-parallel algorithms to process multiple classes simultaneously
- Perform AND/OR/NOT operations on multiple vectors at once
- Map to HVM's natural parallelism

## Performance Advantages for HVM

1. **Natural Parallelism**: HVM evaluates multiple state transitions simultaneously without explicit parallelism primitives

2. **Superposition Benefits**: HVM can explore multiple execution paths in parallel, perfect for NFA state tracking

3. **Pattern Coherence**: Similar patterns can share computation through HVM's evaluation model

4. **Memory Locality**: HVM's evaluation strategy allows for better cache efficiency with properly designed data structures

5. **Scalability**: The approach scales well with more patterns (hundreds or thousands), unlike traditional approaches that slow down linearly

## Practical Application: IDS/IPS

This architecture is particularly well-suited for:

- Network intrusion detection (Snort-like rules)
- Content filtering and classification
- Log analysis with multiple patterns
- Real-time streaming data analysis

## Implementation Considerations

1. **Pattern Preprocessing**: Invest computation in pattern analysis and optimization at setup time, not during matching

2. **State Representation**: Use compact, efficient representations for states and transitions

3. **Memory Management**: Minimize allocation during matching phase

4. **Vectorization**: Design data structures to exploit bit-level parallelism where possible

5. **C Integration**: Use `@extern` for performance-critical operations like character handling and bit operations

## Expected Performance Characteristics

- Setup time: O(m), where m is the total size of all patterns
- Matching time: O(n), where n is the input length
- Space complexity: O(m)
- Parallelism benefit: Grows with the number of patterns

This architecture transforms what is traditionally a weakness (many patterns = slower matching) into a strength by leveraging HVM's natural ability to evaluate multiple paths simultaneously.