#!/usr/bin/env python3
"""
Test the regex parser and matcher implementation
"""

import unittest
import subprocess
import tempfile
import os

class TestRegexParser(unittest.TestCase):
    """Test cases for the regex parser and matcher."""
    
    def test_simple_patterns(self):
        """Test parsing and matching simple patterns."""
        test_cases = [
            # pattern, text, expected_match
            ("a", "a", True),         # Literal
            ("a", "b", False),        # Non-matching literal
            ("ab", "ab", True),       # Concatenation
            ("ab", "ac", False),      # Non-matching concatenation
            ("a|b", "a", True),       # Alternation - first option
            ("a|b", "b", True),       # Alternation - second option
            ("a|b", "c", False),      # Non-matching alternation
            ("a*", "", True),         # Star - zero occurrences
            ("a*", "a", True),        # Star - one occurrence
            ("a*", "aaa", True),      # Star - multiple occurrences
            ("a+", "", False),        # Plus - zero occurrences (no match)
            ("a+", "a", True),        # Plus - one occurrence
            ("a+", "aaa", True),      # Plus - multiple occurrences
            ("a?", "", True),         # Optional - zero occurrences
            ("a?", "a", True),        # Optional - one occurrence
            (".", "x", True),         # Any character
            ("[abc]", "a", True),     # Character class - match
            ("[abc]", "d", False),    # Character class - no match
            ("[^abc]", "d", True),    # Negated character class - match
            ("[^abc]", "a", False),   # Negated character class - no match
            ("(a)", "a", True),       # Group
            ("(a|b)", "b", True),     # Group with alternation
            ("a(b|c)*d", "ad", True), # Complex pattern - zero repetitions in group
            ("a(b|c)*d", "abcd", True), # Complex pattern - multiple repetitions
            ("a(b|c)*d", "abcbcd", True), # Complex pattern - more repetitions
            ("a(b|c)*d", "aed", False),  # Complex pattern - no match
        ]
        
        for pattern, text, expected_match in test_cases:
            result = self.run_hvml_regex(pattern, text)
            if expected_match:
                self.assertTrue(result.startswith("Matched:"), 
                               f"Pattern '{pattern}' should match '{text}', but got: {result}")
            else:
                self.assertEqual(result, "No match", 
                               f"Pattern '{pattern}' should not match '{text}', but got: {result}")
    
    def run_hvml_regex(self, pattern, text):
        """Run the regex parser/matcher with the given pattern and text."""
        # Create a temporary HVML file for this test
        with tempfile.NamedTemporaryFile(suffix=".hvml", mode="w", delete=False) as f:
            test_file = f.name
            # Read the regex_parser.hvml content
            with open("regex_parser.hvml", "r") as parser_file:
                parser_content = parser_file.read()
            
            # Create test-specific code
            test_code = f"""
@main =
  ! pattern = "{pattern}"
  ! text = "{text}"
  
  // Parse and match
  ! result = @match_regex(pattern, text, 0)
  
  ~(== result.1 -1) {{
    1: "No match"
    0: (+ "Matched: " result.0)
  }}
"""
            # Combine parser content with test code
            hvml_code = parser_content + "\n" + test_code
            f.write(hvml_code)
        
        try:
            # Run the HVML file
            hvml_path = "hvml"  # Assuming 'hvml' is in PATH
            
            result = subprocess.run(
                [hvml_path, "run", test_file],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Extract the output
            output = result.stdout.strip()
            # Print debugging info
            print(f">> Pattern: '{pattern}', Text: '{text}'")
            print(f">> Output: {output}")
            print(f">> Stderr: {result.stderr}")
            return output
            
        finally:
            # Clean up the temporary file
            os.unlink(test_file)

def run_tests():
    """Run the regex parser tests."""
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRegexParser)
    result = runner.run(suite)
    
    print(f"\nSummary: Ran {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    import sys
    sys.exit(run_tests())