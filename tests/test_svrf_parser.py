"""
Unit tests for svrf_parser.

This file uses Python's built-in unittest framework to test the functionality of the svrf_parser module.
Each test case ensures that individual functions and components behave as expected.

Usage:
    python -m unittest svrf_parser.py
"""


import unittest
from src.svrf_parser import parse_svrf_rules
import tempfile

class TestSVRFParser(unittest.TestCase):
    def test_parse_svrf_rules(self):
        svrf_data = """
                        //////////////////////////////////
                        ///////////// OPTIONS ////////////
                        //////////////////////////////////
                        LAYOUT SYSTEM GDSII
                        LAYOUT PATH "./regression.gds"
                        LAYOUT PRIMARY TOPCELL
                        DRC RESULTS DATABASE "./drc.db" 
                        DRC SUMMARY REPORT "sum.sum"
                        DRC MAXIMUM RESULTS ALL
                        
                        //////////////////////////////////
                        ///////////// LAYERS /////////////
                        //////////////////////////////////
                        LAYER L 5
                        LAYER M 6
                        
                        
                        //////////////////////////////////
                        ///////////// RULES //////////////
                        //////////////////////////////////
                        
                        L.S.1 {
                            @ Minimum spacing between L >= 0.100
                            EXT L < 0.1 
                        }
                        L.W.1 {
                            @ Minimum width of L >= 0.200
                            INT L < 0.2 
                        }
                        M.A.1 {
                            @ Minimum area of M >= 0.500
                            AREA M < 0.5
                        }
                        
                        M.S.1 {
                            @ Minimum spacing between M >= 0.100
                            EXT M < 0.1 
                        }
                  """
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write(svrf_data)
            f.flush()
            rules = parse_svrf_rules(f.name)

        self.assertEqual(len(rules), 4)
        self.assertEqual(rules[0]["check name"], "L.S.1")
        self.assertIn("Minimum spacing between L >= 0.100", rules[0]["comment"])
        self.assertEqual(rules[1]["check name"], "L.W.1")
        self.assertIn("Minimum width of L >= 0.200", rules[1]["comment"])
        self.assertEqual(rules[2]["check name"], "M.A.1")
        self.assertIn("Minimum area of M >= 0.500", rules[2]["comment"])
        self.assertEqual(rules[3]["check name"], "M.S.1")
        self.assertIn("Minimum spacing between M >= 0.100", rules[3]["comment"])

        
if __name__ == "__main__":
    unittest.main()
