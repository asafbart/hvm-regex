#!/usr/bin/env python3
"""
Test HVM Implementation of Word Boundaries

This script tests the HVM implementation of word boundaries in the regex engine.
"""

import unittest
from hvm_regex_wrapper import HvmRegexMatcher

class TestHvmWordBoundaries(unittest.TestCase):
    """Tests for HVM word boundary patterns."""
    
    def setUp(self):
        """Set up the matcher before each test."""
        # Use the actual HVM implementation (not fallback)
        self.matcher = HvmRegexMatcher(force_fallback=False)
    
    def test_word_boundary(self):
        """Test simple word boundary (\b)."""
        # Basic word boundary patterns
        result = self.matcher.match(r"\b", "word")
        self.assertIsNotNone(result)
        self.assertEqual(result['length'], 0)  # Zero-width assertion
    
    def test_non_word_boundary(self):
        """Test non-word boundary (\B)."""
        # Non-word boundary in the middle of a word
        result = self.matcher.match(r"\B", "word", pos=1)
        self.assertIsNotNone(result)
        self.assertEqual(result['length'], 0)

def run_tests():
    """Run the HVM word boundary tests."""
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHvmWordBoundaries)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report summary
    print(f"\nSummary: Ran {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    import sys
    sys.exit(run_tests())