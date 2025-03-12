#!/usr/bin/env python3
"""
Test script for the optimized HVM regex implementation.
"""

import os
import subprocess
import sys
import json
import unittest

class OptimizedRegexTest(unittest.TestCase):
    """Test suite for the optimized regex implementation."""
    
    def setUp(self):
        """Set up the test environment."""
        self.hvml_file = "optimized_regex.hvml"
        self.hvm_path = "hvml"  # Assumes hvml is in PATH
        self.hvm_regex_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Check if HVM is available
        try:
            subprocess.run([self.hvm_path, "--version"], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        check=False)
        except FileNotFoundError:
            self.skipTest("HVM executable not found in PATH")
    
    def test_literal_match(self):
        """Test literal string matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Literal{\"GET\"}", "GET /index.html", 0)
        
        with open("test_literal.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_literal.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 3, "Match length should be 3")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_literal.hvml"):
                os.remove("test_literal.hvml")
    
    def test_char_match(self):
        """Test single character matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Char{\"a\"}", "abc", 0)
        
        with open("test_char.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_char.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_char.hvml"):
                os.remove("test_char.hvml")
    
    def test_concat_match(self):
        """Test concatenation matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Concat{#Char{\"a\"} #Char{\"b\"}}", "abc", 0)
        
        with open("test_concat.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_concat.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 2, "Match length should be 2")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_concat.hvml"):
                os.remove("test_concat.hvml")
    
    def test_alt_match_first(self):
        """Test alternative pattern matching (first alternative)."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Alt{#Char{\"a\"} #Char{\"b\"}}", "abc", 0)
        
        with open("test_alt_first.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_alt_first.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_alt_first.hvml"):
                os.remove("test_alt_first.hvml")
    
    def test_alt_match_second(self):
        """Test alternative pattern matching (second alternative)."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Alt{#Char{\"x\"} #Char{\"b\"}}", "bcd", 0)
        
        with open("test_alt_second.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_alt_second.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_alt_second.hvml"):
                os.remove("test_alt_second.hvml")
    
    def test_star_match(self):
        """Test star repetition matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Star{#Char{\"a\"}}", "aaab", 0)
        
        with open("test_star.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_star.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 3, "Match length should be 3")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_star.hvml"):
                os.remove("test_star.hvml")
    
    def test_plus_match(self):
        """Test plus repetition matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Plus{#Char{\"a\"}}", "aaab", 0)
        
        with open("test_plus.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_plus.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 3, "Match length should be 3")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_plus.hvml"):
                os.remove("test_plus.hvml")
    
    def test_optional_match(self):
        """Test optional matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Optional{#Char{\"a\"}}", "abc", 0)
        
        with open("test_optional.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_optional.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_optional.hvml"):
                os.remove("test_optional.hvml")
    
    def test_optional_no_match(self):
        """Test optional matching (no match case)."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Optional{#Char{\"x\"}}", "abc", 0)
        
        with open("test_optional_no_match.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_optional_no_match.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 0, "Match length should be 0")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_optional_no_match.hvml"):
                os.remove("test_optional_no_match.hvml")
    
    def test_char_class_match(self):
        """Test character class matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#CharClass{\"abc\"}", "abc", 0)
        
        with open("test_char_class.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_char_class.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_char_class.hvml"):
                os.remove("test_char_class.hvml")
    
    def test_group_match(self):
        """Test group matching."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Group{#Char{\"a\"}}", "abc", 0)
        
        with open("test_group.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_group.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#MatchGroup" in output, f"Expected MatchGroup, got: {output}")
            
            # Extract position, length, group_pos, group_len
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position, length, group_pos, group_len
            self.assertEqual(len(match_details), 4, "MatchGroup should have position, length, group_pos, group_len")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1")
            self.assertEqual(int(match_details[2]), 0, "Group position should be 0")
            self.assertEqual(int(match_details[3]), 1, "Group length should be 1")
            
        finally:
            # Clean up the test file
            if os.path.exists("test_group.hvml"):
                os.remove("test_group.hvml")
    
    def test_positive_lookahead(self):
        """Test positive lookahead assertion."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Concat{#Char{\"a\"} #PosLookahead{#Char{\"b\"}}}", "abc", 0)
        
        with open("test_pos_lookahead.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_pos_lookahead.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1") # Only 'a' is matched, not 'b'
            
        finally:
            # Clean up the test file
            if os.path.exists("test_pos_lookahead.hvml"):
                os.remove("test_pos_lookahead.hvml")
    
    def test_negative_lookahead(self):
        """Test negative lookahead assertion."""
        # Create a temporary HVM file for this test
        test_code = self.generate_test_hvml("#Concat{#Char{\"a\"} #NegLookahead{#Char{\"x\"}}}", "abc", 0)
        
        with open("test_neg_lookahead.hvml", "w") as f:
            f.write(test_code)
        
        try:
            # Run the HVM file
            result = subprocess.run(
                [self.hvm_path, "run", "test_neg_lookahead.hvml"],
                capture_output=True,
                text=True,
                check=False,
            )
            
            # Parse the output
            output = result.stdout.strip()
            self.assertTrue("#Match" in output, f"Expected Match, got: {output}")
            
            # Extract position and length
            pos_start = output.find("{") + 1
            pos_end = output.find("}")
            match_details = output[pos_start:pos_end].strip().split()
            
            # Assert correct position and length
            self.assertEqual(len(match_details), 2, "Match details should have position and length")
            self.assertEqual(int(match_details[0]), 0, "Match position should be 0")
            self.assertEqual(int(match_details[1]), 1, "Match length should be 1") # Only 'a' is matched
            
        finally:
            # Clean up the test file
            if os.path.exists("test_neg_lookahead.hvml"):
                os.remove("test_neg_lookahead.hvml")
                
    def generate_test_hvml(self, pattern, text, pos):
        """Generate HVM code for testing the optimized regex implementation."""
        return f"""// Generated test file for the optimized HVM regex implementation

// Include the entire optimized_regex.hvml file
{open("optimized_regex.hvml").read()}

// Override the main function for testing
@test_main =
  // Test pattern
  ! test_pattern = {pattern}
  ! test_text = "{text}"
  ! test_pos = {pos}
  
  // Run the match
  ! result = @match(test_pattern, test_text, test_pos)
  
  // Return the result
  result

// Use the test main
@main = @test_main
"""

if __name__ == "__main__":
    unittest.main()