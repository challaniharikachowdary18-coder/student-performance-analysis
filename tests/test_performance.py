import unittest
from services.performance import calculate_performance
from utils.validators import validate_marks

class PerformanceTests(unittest.TestCase):
    def test_grade_a_plus_and_pass(self):
        result = calculate_performance([95, 90], 100, 35)
        self.assertEqual(result["grade"], "A+")
        self.assertEqual(result["status"], "Pass")
        self.assertEqual(result["percentage"], 92.5)

    def test_fail_if_any_assessment_below_pass_marks(self):
        result = calculate_performance([80, 20], 100, 35)
        self.assertEqual(result["status"], "Fail")

    def test_empty_scores(self):
        self.assertEqual(calculate_performance([], 100, 35)["status"], "No marks")

    def test_invalid_marks_rejected(self):
        with self.assertRaises(ValueError):
            validate_marks(105, 100)

if __name__ == "__main__":
    unittest.main()
