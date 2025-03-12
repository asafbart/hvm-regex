# HVM3 Development Guide

This document provides guidance on working with HVM3, highlighting common pitfalls, syntax requirements, and best practices based on our experiences. It's intended to help future developers avoid the same mistakes we encountered.

## Strict Syntax Requirements

HVM3 has extremely strict syntax requirements that differ from other functional languages and even from other HVM versions.

### Variable Usage Rules

1. **No Variable Reuse**: HVM3 does not allow using the same variable name in different contexts. Each variable can only be bound once in its scope.

   ```
   // WRONG - reuses variable 'result'
   @match_alt(a b) =
     ! result = @match(a)
     ~ result {
       #Match{len}: result  // Error: variable 'result' reused
       #NoMatch: @match(b)
     }
   
   // CORRECT - uses different variable names
   @match_alt(a b) =
     ! result_a = @match(a)
     ~ result_a {
       #Match{len}: #Match{len}  // Create a new value instead of reusing variable
       #NoMatch: @match(b)
     }
   ```

2. **Pattern Variable Reuse**: Variables can't be reused even in pattern matching.

   ```
   // WRONG - reuses 'count' in arithmetic
   @run(count) = ~ count {
     0: 0
     _: ! new_count = (+ count 1)  // Error: 'count' reused
        @run(new_count)
   }
   
   // CORRECT - uses different variable names
   @run(n) = ~ n {
     0: 0
     _: ! new_n = (+ n 1)
        @run(new_n)
   }
   ```


### Pattern Matching

1. **Nested Patterns**: HVM3 requires careful pattern structure. Deeply nested patterns can cause syntax errors.

2. **Match Exhaustiveness**: Always provide a catch-all case with `_:` to handle unexpected inputs.

3. **Complex Pattern Matching**: Break complex pattern matching into smaller, simpler steps.

   ```
   // WRONG - too complex
   ~ complex_data {
     #Complex{a b #Nested{c d}}: ...
   }
   
   // CORRECT - break it down
   ~ complex_data {
     #Complex{a b nested}: 
       ~ nested {
         #Nested{c d}: ...
       }
   }
   ```

## String Handling

HVM3 has unique requirements for string handling:

1. **String Literals**: String literals must use explicit types and can't be directly pattern-matched.

   ```
   // WRONG - direct string pattern matching
   @strlen(str) = ~ str {
     "": 0
     "a": 1
     // ...
   }
   
   // CORRECT - use enums or character codes
   @strlen(str) = ~ str {
     #Empty: 0
     #A: 1
     // ...
   }
   ```

2. **Character Representation**: Use enums or character codes instead of string literals.

   ```
   // Define character enums
   data Char { #A #B #C #_1 #_2 #_3 }
   
   // Use enums for character matching
   @match_char(c) = ~ c {
     #A: 1
     #B: 1
     #_1: 0
   }
   ```

## Data Structures

1. **List Representation**: Explicitly define list data structures with `Nil` and `Cons` constructors.

   ```
   data List { #Nil #Cons{head tail} }
   ```

2. **Recursive Data Structures**: Carefully define recursive data structures to avoid infinite recursion.

## Function Definitions

1. **Main Function Format**: The main function must follow a specific format to be recognized:

   ```
   @main = ~ (#Pol{123}) {
     #Var{idx}: *
     #Pol{bod}: 
       // Your actual logic here
     #All{inp bod}: *
     #Lam{bod}: *
     #App{fun arg}: *
     #U32: *
     #Num{val}: *
   }
   ```

2. **Function Arguments**: Keep function signatures simple and consistent.

## Testing Approaches

1. **Progressive Testing**: Start with minimal examples that you're confident will work, then incrementally add complexity.

2. **Test Cases**: Create specific test cases for each feature.

3. **Isolation**: When facing errors, isolate the problematic component in a minimal test file.

## Common Error Messages

1. **"key not found: main"**: This usually indicates a syntax error that prevents the parser from reaching the main function definition. Look for variable reuse or pattern matching issues.

2. **"Variable X used more than once"**: A variable is being reused in the same scope. Create a new variable with a different name.

3. **"PARSE_ERROR"**: Syntax error in the code. The error message should point to the problematic line.

## Best Practices

1. **Use Enums for Strings**: Represent string values as enums to avoid string handling issues.

2. **Simple Pattern Matching**: Keep pattern matching simple and break complex patterns into smaller steps.

3. **Unique Variable Names**: Use unique variable names even across different branches of code.

4. **Incremental Development**: Build and test in small increments to isolate issues.

5. **Simplified Functions**: Create simplified versions of complex functions for testing.

## Regex Implementation Best Practices

When implementing regex functionality in HVM3:

1. **Character Representation**: Use enums for character representations rather than string literals.

2. **Pattern Representation**: Define clear data types for different regex components.

3. **Parser Structure**: Break down the parser into distinct phases (tokenization, parsing, AST building).

4. **Matcher Implementation**: Implement matchers for each pattern type separately.

5. **Testing Strategy**: Test each regex feature in isolation before combining.

6. **Error Handling**: Provide meaningful error messages for syntax and matching errors.

## Optimization Techniques

1. **Pattern Caching**: Cache compiled patterns to avoid reparsing.

2. **Early Returns**: Return as soon as a match is found or can be determined to fail.

3. **Character Class Optimization**: Use specialized data structures for character classes.

4. **Avoid Recursion**: Be careful with recursive functions, as they can hit stack limits.

## Debugging Tips

1. **Simplify**: When facing issues, create a minimal example that demonstrates the problem.

2. **Print Intermediate Results**: Use the main function to return intermediate results for inspection.

3. **Step-by-Step**: Break complex operations into smaller steps with explicit intermediate variables.

4. **Check Syntax**: Ensure your syntax follows HVM3's strict requirements.

## Running Tests with HVM3

To run tests for your HVM3 code, you can use the following commands:

### Basic Test Execution

To run a single test file:

```bash
cabal run hvml -- run tests/unit/your_test_file.hvml
```

This will execute the file and display the result. A successful test typically outputs a single value, which is the return value of the `main` function.

### Testing Tips

1. **Test Incrementally**: Start with the simplest possible test case and gradually add complexity.

2. **Isolated Testing**: When facing errors, create minimal test files that isolate the specific feature or behavior you're testing.

3. **Error Diagnosis**: If you encounter parse errors, HVM3 will tell you the line number and a brief description of the issue.

4. **Unit Testing**: Create small functions that test individual components:

   ```
   @test_feature =
     ! input = ...
     ! expected = ...
     ! result = @feature_under_test(input)
     (== result expected)  // Returns 1 if test passes, 0 if it fails
   ```

5. **Combining Test Results**: You can combine multiple test results using the logical AND operator:

   ```
   @main = ~ (#Pol{123}) {
     #Var{idx}: *
     #Pol{bod}:
       ! test1 = @test_feature1
       ! test2 = @test_feature2
       (& test1 test2)  // Returns 1 only if both tests pass
     ...
   }
   ```

### Debugging Failed Tests

When a test fails:

1. Check for syntax errors in your test code
2. Verify that your `main` function follows the required format
3. Look for variable reuse issues
4. Ensure pattern matching is exhaustive
5. Break complex operations into simpler steps with intermediate variables

## Conclusion

HVM3 is powerful but has strict requirements. By following these guidelines, you can avoid common pitfalls and build reliable, efficient code. Always start simple, test incrementally, and follow the exact syntax patterns that are known to work with your HVM3 installation.