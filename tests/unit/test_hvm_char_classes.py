#!/usr/bin/env python3
"""
Test HVM Implementation of Character Classes

This script tests the HVM implementation of character classes in the regex engine.
"""

import unittest
from hvm_regex_wrapper import HvmRegexMatcher

class TestHvmCharClasses(unittest.TestCase):
    """Tests for HVM character class patterns."""
    
    def setUp(self):
        """Set up the matcher before each test."""
        # Use the actual HVM implementation (not fallback)
        self.matcher = HvmRegexMatcher(force_fallback=False)
    
    def test_simple_char_class(self):
        """Test basic character class [abc]."""
        # Should match first character
        result = self.matcher.match("[abc]", "abc")
        self.assertIsNotNone(result)
        self.assertEqual(result['position'], 0)
        self.assertEqual(result['length'], 1)
    
    def test_digit_char_class(self):
        """Test digit character class [0-9]."""
        # Should match digits
        result = self.matcher.match("[0-9]", "123")
        self.assertIsNotNone(result)
        self.assertEqual(result['position'], 0)
        self.assertEqual(result['length'], 1)
    
    def test_alpha_char_class(self):
        """Test alphabetic character class [a-z]."""
        # Should match lowercase letters
        result = self.matcher.match("[a-z]", "abc")
        self.assertIsNotNone(result)
        self.assertEqual(result['position'], 0)
        self.assertEqual(result['length'], 1)
    
    def test_negated_char_class(self):
        """Test negated character classes [^abc]."""
        # Should match characters not in the class
        result = self.matcher.match("[^abc]", "xyz")
        self.assertIsNotNone(result)
        self.assertEqual(result['position'], 0)
        self.assertEqual(result['length'], 1)

def run_tests():
    """Run the character class tests with HVM implementation."""
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHvmCharClasses)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report summary
    print(f"\nSummary: Ran {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    import sys
    sys.exit(run_tests())