# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

from tiebreak import tiebreak
from tests.fixtures import (
    make_game,
    make_competitor,
    make_individual_tournament,
    tiebreak_params,
)


class TestTiebreak(unittest.TestCase):
    def _run(self, tournament=None, tiebreaks=None, current_round=-1):
        tm = tournament or make_individual_tournament()
        params = tiebreak_params(tiebreaks=tiebreaks or ["PTS", "BH", "SNO"], current_round=current_round)
        tb = tiebreak(tm, params["current_round"], params)
        return tb.compute_tiebreaks(tm, params)

    def test_points_ranking(self):
        result = self._run()
        by_cid = {c["cid"]: c for c in result["competitors"]}
        # Player 1: W+W+D = 2.5 ; Player 3: D+L+W = 1.5 ; Player 2: L+W+L = 1.0 ; Player 4: D+L+D = 1.0
        self.assertEqual(by_cid[1]["tiebreakScore"][0], Decimal("2.5"))
        self.assertEqual(by_cid[1]["rank"], 1)

    def test_current_round_filter(self):
        # After round 1 only: 1 has 1.0, 3 and 4 have 0.5, 2 has 0.0
        result = self._run(current_round=1, tiebreaks=["PTS", "SNO"])
        by_cid = {c["cid"]: c for c in result["competitors"]}
        self.assertEqual(by_cid[1]["tiebreakScore"][0], Decimal("1.0"))
        self.assertEqual(by_cid[2]["tiebreakScore"][0], Decimal("0.0"))
        self.assertEqual(by_cid[3]["tiebreakScore"][0], Decimal("0.5"))

    def test_buchholz_present(self):
        result = self._run(tiebreaks=["PTS", "BH"])
        for cmp in result["competitors"]:
            self.assertEqual(len(cmp["tiebreakScore"]), 2)
            self.assertIsNotNone(cmp["tiebreakScore"][0])

    def test_direct_encounter(self):
        # Two players tied on points with a mutual game
        competitors = [make_competitor(i) for i in range(1, 3)]
        games = [make_game(1, 1, 2, "W")]
        tm = make_individual_tournament(num_rounds=1, competitors=competitors, games=games)
        result = self._run(tournament=tm, tiebreaks=["PTS", "DE", "SNO"])
        by_cid = {c["cid"]: c for c in result["competitors"]}
        self.assertEqual(by_cid[1]["rank"], 1)
        self.assertEqual(by_cid[2]["rank"], 2)

    def test_empty_tournament_does_not_crash(self):
        tm = make_individual_tournament(competitors=[], games=[], num_rounds=0)
        params = tiebreak_params(tiebreaks=["PTS"])
        # Empty competitors may still construct; ensure compute is safe
        if not tm["competitors"]:
            tm["competitors"] = []
            tb = tiebreak(tm, -1, params)
            result = tb.compute_tiebreaks(tm, params)
            self.assertEqual(result["competitors"], [])

    def test_rules_version_pre_2024(self):
        tm = make_individual_tournament(start_date="2023-01-01")
        params = tiebreak_params()
        tb = tiebreak(tm, -1, params)
        tb.find_tmversion(tm)
        self.assertEqual(tb.rulesversion, 0)

    def test_rules_version_2024(self):
        tm = make_individual_tournament(start_date="2025-01-01")
        params = tiebreak_params()
        tb = tiebreak(tm, -1, params)
        tb.find_tmversion(tm)
        self.assertEqual(tb.rulesversion, 1)

    def test_get_score_derives_from_opponent_side(self):
        tm = make_individual_tournament()
        params = tiebreak_params()
        tb = tiebreak(tm, -1, params)
        result = {"black": 2, "bResult": "L", "played": True}
        score = tb.get_score(tb.gamescore, result, "white")
        self.assertEqual(score, Decimal("1.0"))  # reverse of L is W


if __name__ == "__main__":
    unittest.main()
