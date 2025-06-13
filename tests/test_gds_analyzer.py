"""
Unit tests for gds_analyzer.

This file uses Python's built-in unittest framework to test the functionality of the gds_analyzer module.
Each test case ensures that individual functions and components behave as expected.

Usage:
    python -m unittest test_gds_analyzer.py
"""


import unittest
from src.gds_analyzer import extract_markers, find_text_labels, find_rule_groups, patterns_in_polygon, associate_rules_to_patterns
from src.utils.create_gds import create_test_layout_cell


class TestGDSAnalyzer(unittest.TestCase):

    def setUp(self):
        self.cell=create_test_layout_cell()

    def test_extract_markers(self):
        markers = extract_markers(self.cell).get((0, 1), [])
        layer_numbers = list(map(lambda x: x.layer, markers))
        datatypes = list(map(lambda x: x.datatype, markers))
        self.assertTrue(layer_numbers==[0, 0], "Incorrect layer numbers")
        self.assertTrue(datatypes==[1, 1], "Incorrect datatypes")

    def test_find_text_labels(self):
        text_labels = find_text_labels(self.cell)
        self.assertTrue(text_labels[0]['text']=="check_name", "Incorrect rule name")
        self.assertTrue(text_labels[0]['position']==(0.0, -0.5), "Incorrect rule label position")

    def test_find_rule_groups(self):
        rule_groups = find_rule_groups(self.cell)  # polygons on 255.1
        layer_numbers = list(map(lambda x: x.layer, rule_groups))
        datatypes = list(map(lambda x: x.datatype, rule_groups))
        self.assertTrue(layer_numbers[0]==255, "Incorrect rule grouping layer number")
        self.assertTrue(datatypes[0]==1, "Incorrect rule grouping layer datatype")

    def test_patterns_in_polygon(self):
        group_poly = find_rule_groups(self.cell)[0]
        contained_patterns = len(patterns_in_polygon(self.cell.polygons, group_poly))
        self.assertTrue(contained_patterns==15, "Incorrect number of contained polygons in the rule group")

    def test_associate_rules_to_patterns(self):
        rule_map = associate_rules_to_patterns(self.cell)
        rule_name, polys = next(iter(rule_map.items()))
        layer_no = list(map(lambda x: x.layer, polys))
        datatypes = list(map(lambda x: x.datatype, polys))
        self.assertTrue(rule_name=="check_name", "Incorrect rule name")
        self.assertTrue(layer_no==[255, 255, 255, 255], "Incorrect associated layer numbers")
        self.assertTrue(datatypes==[0, 0, 0, 0], "Incorrect associated datatypes")

if __name__ == "__main__":
    unittest.main()
