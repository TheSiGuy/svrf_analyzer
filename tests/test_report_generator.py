import os
import unittest
from pathlib import Path
import pandas as pd
from src.report_generator import generate_reports


class TestGenerateReports(unittest.TestCase):

    def setUp(self):
        self.output_dir = "test_output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.report_type="both"

        self.summary = {
            "Host Name": "unit-test-host",
            "Timestamp": "2025-06-10 12:34:56",
            "Input Files": "test.svrf, test.gds",
            "Overall Status": "Passed"
        }

        self.details = [
            {
                "Rule Name": "Rule1",
                "Good Patterns": 10,
                "Bad Patterns": 5,
                "Passed Good": 10,
                "Failed Good": 0,
                "Passed Bad": 0,
                "Failed Bad": 5,
                "Rule Comment": "Test rule",
                "Fail Pattern Location": "file.gds, CellX"
            }
        ]

    def test_report_files_created(self):
        html_path, excel_path = generate_reports(self.summary, self.details, self.output_dir, self.report_type, "None")

        # Check that files exist
        if self.report_type=="html" or self.report_type=="both":
            self.assertTrue(Path(html_path).is_file(), "HTML report not created")
        else:
            pass

        if self.report_type=="excel" or self.report_type=="both":
            self.assertTrue(Path(excel_path).is_file(), "Excel report not created")
        else:
            pass


        # Basic HTML content check
        if self.report_type == "html" or self.report_type == "both":
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("<html>", content)
                self.assertIn("SVRF Layout Analysis Report", content)
                self.assertIn("Rule1", content)
        else:
            pass

        # Basic Excel content check
        if self.report_type == "excel" or self.report_type == "both":
            df = pd.read_excel(excel_path, sheet_name=None)
            self.assertIn("Summary", df)
            self.assertIn("Detailed Results", df)
            self.assertFalse(df["Summary"].empty)
            self.assertFalse(df["Detailed Results"].empty)
        else:
            pass

    def tearDown(self):
        # Clean generated test files
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)


if __name__ == "__main__":
    unittest.main()
