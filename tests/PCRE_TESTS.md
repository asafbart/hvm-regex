# PCRE Regex Test Plan

This document outlines our plan for creating comprehensive tests for the HVM3-compatible regex implementation with a focus on PCRE (Perl Compatible Regular Expressions) compatibility.

## Test Categories

1. **Basic PCRE Features**
   - Simple patterns with literals, concatenation
   - Basic repetition operators: `*`, `+`, `?`
   - Character classes: `[a-z]`, `[^0-9]`
   - Alternation: `a|b`
   - Grouping: `(ab)+`
   - Anchors: `^`, `$`

2. **Extended PCRE Features**
   - Lazy quantifiers: `*?`, `+?`, `??`
   - Possessive quantifiers: `*+`, `++`, `?+`
   - Backreferences: `\1`, `\2`, etc.
   - Named capture groups: `(?<name>...)`
   - Non-capturing groups: `(?:...)`
   - Atomic groups: `(?>...)`
   - Lookahead: `(?=...)`, `(?!...)`
   - Lookbehind: `(?<=...)`, `(?<!...)`

3. **Character Class Shortcuts**
   - `\d` - Digits
   - `\w` - Word characters
   - `\s` - Whitespace
   - `\D`, `\W`, `\S` - Negated versions
   - POSIX character classes: `[:alpha:]`, `[:digit:]`, etc.

4. **Special Features**
   - Unicode support
   - Multiline mode
   - Case-insensitive matching
   - DOTALL mode (`.` matches newline)
   - Extended mode (ignore whitespace)

## Real-World Examples

Test patterns from common use cases:
1. Email validation
2. URL matching
3. IP address validation
4. Date/time formats
5. Credit card number validation
6. Phone number matching
7. HTML tag parsing
8. Log file parsing

## Performance Tests

1. **Pattern Complexity**
   - Simple patterns (few operations)
   - Medium complexity (10-20 operations)
   - Complex patterns (20+ operations with various features)

2. **Input Size**
   - Small inputs (< 100 characters)
   - Medium inputs (100-10,000 characters)
   - Large inputs (> 10,000 characters)

3. **Common Bottlenecks**
   - Backtracking with nested repetition
   - Catastrophic backtracking cases
   - Character class performance
   - Alternation with similar prefixes

## Test Structure

Each test will include:
1. The regex pattern
2. Test input strings (both matching and non-matching)
3. Expected results (match positions, captured groups)
4. Performance metrics (matching time)

## Implementation Priority

1. Implement basic PCRE features first
2. Add real-world example tests
3. Add performance tests
4. Gradually add extended PCRE features

## Tools

Create tools to:
1. Generate test cases from patterns and inputs
2. Run performance benchmarks
3. Compare results with reference PCRE implementations
4. Generate reports on compatibility and performance