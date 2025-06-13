"""
Unit tests for pattern_validator.

This file uses Python's built-in unittest framework to test the functionality of the pattern_validator module.
Each test case ensures that individual functions and components behave as expected.

Usage:
    python -m unittest test_pattern_validator.py
"""


import unittest
from src.pattern_validator import validate_patterns
from src.utils.create_gds import create_test_layout_cell
from src.gds_analyzer import extract_markers, find_text_labels,associate_rules_to_patterns

class TestPatternValidator(unittest.TestCase):
    def test_validate_patterns(self):

        cell = create_test_layout_cell()
        rule_name = find_text_labels(cell)[0]['text']
        rule_map = associate_rules_to_patterns(cell)
        markers = extract_markers(cell).get((0, 1), [])
        patterns_for_rule = rule_map.get(rule_name, [])
        result = validate_patterns(rule_name, patterns_for_rule, markers)

        self.assertEqual(result["good"]["pass"], 1)
        self.assertEqual(result["good"]["fail"], 1)
        self.assertEqual(result["bad"]["pass"], 1)
        self.assertEqual(result["bad"]["fail"], 1)



if __name__ == "__main__":
    unittest.main()
