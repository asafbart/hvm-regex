#!/usr/bin/env python3
"""
Test HVM Implementation of Capturing Groups

This script tests the HVM implementation of capturing groups in the regex engine.
"""

import unittest
from hvm_regex_wrapper import HvmRegexMatcher

class TestHvmGroups(unittest.TestCase):
    """Tests for HVM capturing groups."""
    
    def setUp(self):
        """Set up the matcher before each test."""
        # Use the actual HVM implementation (not fallback)
        self.matcher = HvmRegexMatcher(force_fallback=False)
    
    def test_simple_group(self):
        """Test simple capturing groups (a)."""
        # Single character in a group
        result = self.matcher.match("(a)", "abc")
        self.assertIsNotNone(result)
        self.assertEqual(result['length'], 1)
        # Check that groups exists in the result
        self.assertIn('groups', result)
    
    def test_literal_group(self):
        """Test capturing group with literals (GET)."""
        # Group containing a literal
        result = self.matcher.match("(GET)", "GET /index.html")
        self.assertIsNotNone(result)
        self.assertIn('groups', result)
    
    def test_concat_group(self):
        """Test capturing group with concatenation (ab)."""
        # Group containing concatenation
        result = self.matcher.match("(ab)", "abc")
        self.assertIsNotNone(result)
        self.assertIn('groups', result)
    
    def test_backreference(self):
        """Test backreferences \\1."""
        # Pattern with backreference to repeat the captured group
        result = self.matcher.match(r"(a)\1", "aabcd")
        self.assertIsNotNone(result)
        self.assertIn('groups', result)

def run_tests():
    """Run the HVM capturing groups tests."""
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHvmGroups)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Report summary
    print(f"\nSummary: Ran {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    import sys
    sys.exit(run_tests())