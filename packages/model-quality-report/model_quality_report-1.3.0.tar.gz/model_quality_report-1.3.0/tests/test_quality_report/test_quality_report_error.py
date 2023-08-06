import unittest

from model_quality_report.quality_report.quality_report_error import QualityReportError


class TestQualityReportError(unittest.TestCase):
    def test_error_object_is_initially_empty(self):
        error = QualityReportError()
        self.assertTrue(error.is_empty())

    def test_is_empty_returns_false_after_adding_errors(self):
        error = QualityReportError()

        error.add("This does not work")
        self.assertFalse(error.is_empty())

        error.add("This also does not work")
        self.assertFalse(error.is_empty())
        self.assertTrue(len(error.error_list) == 2)

    def test_to_string_method_returns_string(self):
        error = QualityReportError()

        error.add("This does not work")
        self.assertFalse(error.is_empty())

        error.add("This also does not work")
        self.assertTrue(isinstance(error.to_string(), str))
