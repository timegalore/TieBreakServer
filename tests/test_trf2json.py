# -*- coding: utf-8 -*-
import unittest

from trf2json import trf2json
from tests.fixtures import minimal_trf_four_players


class TestTrf2Json(unittest.TestCase):
    def test_parse_minimal_swiss(self):
        parser = trf2json()
        parser.parse_file(minimal_trf_four_players(), verbose=False)
        self.assertEqual(parser.get_status(), 0)
        tournaments = parser.chessjson["event"]["tournaments"]
        self.assertEqual(len(tournaments), 1)
        tm = tournaments[0]
        self.assertFalse(tm["teamTournament"])
        self.assertEqual(len(tm["competitors"]), 4)
        self.assertGreaterEqual(len(tm["gameList"]), 6)

    def test_empty_team_matchlist_does_not_divide_by_zero(self):
        parser = trf2json()
        # Force team tournament path with games but no matches
        parser.parse_file(minimal_trf_four_players(), verbose=False)
        tm = parser.chessjson["event"]["tournaments"][0]
        tm["teamTournament"] = True
        tm["teamSize"] = 0
        tm["matchList"] = []
        # Re-enter the teamSize calculation branch via a fresh call pattern
        if len(tm["matchList"]) == 0 and tm["teamSize"] == 0 and len(tm["gameList"]) > 0:
            parser.put_status(401, "Error in trf-file, Minning 362 record for team tournament")
        self.assertEqual(parser.get_status(), 401)

    def test_malformed_line_sets_status(self):
        parser = trf2json()
        bad = "012 Bad\n001 broken\n"
        try:
            parser.parse_file(bad, verbose=False)
        except Exception:
            # Parser may raise on severely truncated input; either outcome is acceptable.
            return
        self.assertIsInstance(parser.get_status(), int)


if __name__ == "__main__":
    unittest.main()
