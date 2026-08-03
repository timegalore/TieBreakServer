# -*- coding: utf-8 -*-
import unittest

import helpers


class TestParseDate(unittest.TestCase):
    def test_iso_dot_date(self):
        self.assertEqual(helpers.parse_date("2024.08.03"), "2024-08-03")

    def test_eu_dot_date(self):
        self.assertEqual(helpers.parse_date("03.08.2024"), "2024-08-03")

    def test_eu_slash_four_digit_year(self):
        self.assertEqual(helpers.parse_date("03/08/2024"), "2024-08-03")

    def test_eu_slash_two_digit_year(self):
        self.assertEqual(helpers.parse_date("03/08/24"), "2024-08-03")

    def test_iso_slash_date(self):
        self.assertEqual(helpers.parse_date("2024/08/03"), "2024-08-03")


class TestParseNumbers(unittest.TestCase):
    def test_parse_int_blank(self):
        self.assertEqual(helpers.parse_int("   "), 0)

    def test_parse_int_value(self):
        self.assertEqual(helpers.parse_int(" 42 "), 42)

    def test_parse_float_blank(self):
        self.assertEqual(helpers.parse_float(""), helpers.parse_float("0.0"))

    def test_parse_float_comma(self):
        self.assertEqual(helpers.parse_float("1,5"), helpers.parse_float("1.5"))


class TestFileFormat(unittest.TestCase):
    def test_trf_ext(self):
        self.assertEqual(helpers.getFileFormat("event.trf"), "TRF")

    def test_json_ext(self):
        fmt = helpers.getFileFormat("event.json")
        self.assertIn(fmt, ("JSON", "JCH"))


class TestSafe(unittest.TestCase):
    def test_safe_nested(self):
        data = {"a": {"b": 3}}
        self.assertEqual(helpers.safe([data], ["a", "b"]), 3)

    def test_safe_missing(self):
        self.assertIsNone(helpers.safe([{}], ["a", "b"]))


if __name__ == "__main__":
    unittest.main()
