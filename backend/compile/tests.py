from django.test import TestCase
import json
import os
import tempfile

from .DriverCode import PythonDriverCode, CppDriverCode, CDriverCode
from .ExecuteCode import write_testcases_json, _TESTCASES_FILENAME, ExecuteInPython


class WriteTestcasesJsonHelperTests(TestCase):
    """Tests for write_testcases_json helper in ExecuteCode."""

    def test_writes_file_to_temp_dir(self):
        test_cases = {"method_name": "add", "cases": [{"input": [1, 2], "expected": 3}]}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_testcases_json(tmpdir, test_cases)
            self.assertTrue(os.path.exists(path))
            self.assertEqual(os.path.basename(path), _TESTCASES_FILENAME)
            with open(path) as f:
                loaded = json.load(f)
            self.assertEqual(loaded, test_cases)

    def test_custom_filename(self):
        test_cases = {"cases": []}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_testcases_json(tmpdir, test_cases, filename="custom.json")
            self.assertTrue(os.path.exists(path))
            self.assertEqual(os.path.basename(path), "custom.json")

    def test_returns_full_path(self):
        test_cases = {"cases": []}
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_testcases_json(tmpdir, test_cases)
            self.assertTrue(os.path.isabs(path))
            self.assertTrue(path.startswith(tmpdir))


class PythonDriverCodeTests(TestCase):
    """Tests for the updated PythonDriverCode.DriverCodeGenerator."""

    def _make_test_cases(self):
        return {
            "method_name": "add",
            "cases": [{"input": [1, 2], "expected": 3}],
        }

    def test_uses_json_file_path(self):
        gen = PythonDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn('"testcases.json"', gen)

    def test_imports_json(self):
        gen = PythonDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("import json as _json", gen)

    def test_reads_from_file(self):
        gen = PythonDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("open(", gen)
        self.assertIn("_json.load", gen)

    def test_iterates_cases(self):
        gen = PythonDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn('_data["cases"]', gen)

    def test_error_message_format(self):
        gen = PythonDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("Error at test case", gen)

    def test_accepted_message(self):
        gen = PythonDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("Accepted", gen)


class CppDriverCodeTests(TestCase):
    """Tests for the updated CppDriverCode.DriverCodeGenerator."""

    def _make_test_cases(self):
        return {
            "method_name": "add",
            "return_type": "int",
            "signature": ["int", "int"],
            "cases": [{"input": [1, 2], "expected": 3}],
        }

    def test_uses_json_file_path(self):
        gen = CppDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn('"testcases.json"', gen)

    def test_includes_fstream(self):
        gen = CppDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("#include <fstream>", gen)

    def test_uses_ifstream(self):
        gen = CppDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("ifstream", gen)

    def test_uses_json_parse(self):
        gen = CppDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("json::parse", gen)

    def test_no_raw_string_literal(self):
        gen = CppDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertNotIn('R"(', gen)

    def test_error_message_format(self):
        gen = CppDriverCode().DriverCodeGenerator("", self._make_test_cases(), "testcases.json")
        self.assertIn("Error at test case", gen)


class PythonExecuteEndToEndTests(TestCase):
    """End-to-end tests for Python execution with JSON file-based test cases."""

    def _make_test_cases(self):
        return {
            "method_name": "add",
            "cases": [
                {"input": [1, 2], "expected": 3},
                {"input": [10, 20], "expected": 30},
            ],
        }

    def test_accepted_on_correct_solution(self):
        user_code = "class Solution:\n    def add(self, a, b):\n        return a + b\n"
        full_code = PythonDriverCode().DriverCodeGenerator(user_code, self._make_test_cases(), "testcases.json")
        result = ExecuteInPython().Execute(full_code, "solution.py", self._make_test_cases())
        self.assertEqual(result["output"], "Accepted")
        self.assertEqual(result["errors"], "")

    def test_error_on_wrong_answer(self):
        bad_cases = {
            "method_name": "add",
            "cases": [
                {"input": [1, 2], "expected": 3},
                {"input": [1, 1], "expected": 99},  # will fail
            ],
        }
        user_code = "class Solution:\n    def add(self, a, b):\n        return a + b\n"
        full_code = PythonDriverCode().DriverCodeGenerator(user_code, bad_cases, "testcases.json")
        result = ExecuteInPython().Execute(full_code, "solution.py", bad_cases)
        self.assertIn("Error at test case 2", result["output"])

