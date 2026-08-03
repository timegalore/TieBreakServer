# -*- coding: utf-8 -*-
import unittest

from pairingdutch import pairing_dutch
from pairingberger import pairing_berger
from tests.fixtures import make_competitor, make_individual_tournament


class TestPairing(unittest.TestCase):
    def _fresh_tournament(self, n=6):
        competitors = [make_competitor(i, rating=2200 - i * 5, present=True) for i in range(1, n + 1)]
        return make_individual_tournament(
            num_rounds=n - 1 if n % 2 == 0 else n,
            competitors=competitors,
            games=[],
            tournament_type="Swiss",
        )

    def test_dutch_round_one_pairs_everyone(self):
        tm = self._fresh_tournament(6)
        tm["pairingSystem"] = ["dutch"]
        params = {
            "experimental": [],
            "verbose": 0,
            "top_color": "w",
            "rank": False,
        }
        engine = pairing_dutch(tm, 1, params)
        pairs = engine.compute_pairing(checkonly=False, reportlevel=0)
        self.assertIsInstance(pairs, list)
        # roundpairing brackets with pairs covering 6 players => 3 boards
        boarded = []
        for bracket in pairs:
            for p in bracket.get("pairs", []):
                boarded.append((p.get("w"), p.get("b")))
        players = []
        for w, b in boarded:
            if w:
                players.append(w)
            if b:
                players.append(b)
        self.assertEqual(sorted(players), [1, 2, 3, 4, 5, 6])

    def test_topcolor_is_deterministic(self):
        tm = self._fresh_tournament(4)
        tm.pop("topColor", None)
        params = {"experimental": [], "verbose": 0, "top_color": "", "rank": False}
        a = pairing_dutch(tm, 1, params).topcolor
        b = pairing_dutch(tm, 1, params).topcolor
        self.assertEqual(a, b)
        self.assertEqual(a, "w")

    def test_berger_skips_absent(self):
        tm = self._fresh_tournament(4)
        tm["tournamentType"] = "Round Robin"
        tm["pairingSystem"] = ["berger"]
        tm["competitors"][2]["present"] = False  # cid 3
        # Ensure rfp comes from present via crosstable; berger uses competitors[].rfp from engine
        params = {"experimental": [], "verbose": 0, "top_color": "w", "rank": False}
        engine = pairing_berger(tm, 1, params)
        # Mark rfp on engine competitors after init by computing pairing
        pairs = engine.compute_pairing(checkonly=False, reportlevel=0)
        self.assertIsInstance(pairs, list)
        boarded = []
        for bracket in pairs:
            for p in bracket.get("pairs", []):
                boarded.append((p.get("w"), p.get("b")))
        for w, b in boarded:
            self.assertNotEqual(w, 3)
            self.assertNotEqual(b, 3)


if __name__ == "__main__":
    unittest.main()
